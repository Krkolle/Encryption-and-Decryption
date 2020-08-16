#You can find the modules required for this program to run in 'requirements.txt' Install the packages first and then proceed with below changes.

#Changes to be made in the file before running it :
#1 . Whereever it is mentioned 'sender_mail_id', type in your mail ID or the test mail if you have created one.
#2 . If you are using GMAIL to send mails, then you can go ahead with the same smtp configuration.
#In case of others, find their SMTP Servers and ports used and update in the line where it says 'smtp.gmail.com'
#3. If you are using Gmail, you will either have to create an app password. # Generate an app password you have generated from Google. Visit 'https://bit.ly/googleapppasswords' to create one.\
#If you already have an app password, you can use the same. And enter the same whereever it says 'Application_Password'
#4. While running the code for the first time, ensure that 'dbase.json' is present in the same directory. dbase.json should have one entry as shown in the repository file.

#Steps to encrypt and decrypt
#1. As of now, I have tested this code for text files only. So to encrypt a new file, create a text file in the same directory. And then follow the steps as mentioned.
#2. If you would like to decrypt an encrypted file, ensure that .aes file is present in the directory. Keep your encryption password handy. Without that you cannot access your encrypted file.

#Note : If you plan on uploading your script to GitHub or any other location, ensure that you don't mention your sender_mail_id and Application_Password in the file.
#If at all you do upload it, those who get access to the repository will be able to send mails using the credentials. 

#If you face issues while implementing this code, or sending mails to multiple users, feel free to reach out to me at 'krkolle@gmail.com'
import datetime, os, json, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet
import math, random
from Crypto import Random
import pyAesCrypt
from os import stat, remove
from Crypto.Cipher import AES
def decryption_mail_send(otp_number,toaddress):
    msg = MIMEMultipart() 
    msg['From'] ='sender_mail_id' #Enter the mail ID from which you would like to send this mail.
    x = datetime.datetime.now()
    msg['Subject'] = "Decrypt Request at " + str(x)
    body = "Hello, We got a request to decrypt your data. Below is your OTP. \n" + str(otp_number) + "\n Use it in the console to decrypt your data"
    msg.attach(MIMEText(body, 'plain'))
    p = MIMEBase('application', 'octet-stream') 
    s = smtplib.SMTP('smtp.gmail.com', 587) #Depending on the smtp server, you will have to change this. 587 is the port number for smtp.gmail.com
    s.starttls()
    s.login('sender_mail_id', "Application_Password") # Generate an app password you have generated from Google. If you don't have one, visit 'https://bit.ly/googleapppasswords' to create one.
    text = msg.as_string()
    s.sendmail('sender_mail_id', toaddress, text) 
    s.quit() 
 
def encryption_mail_send(toaddress,file_name,password):
    msg = MIMEMultipart() 
    msg['From'] ='sender_mail_id ' #Enter the mail ID from which you would like to send this mail.
    msg['Subject'] = "Encrypted File " + file_name
    body = "Hello, We have encrypted the file as per your request. Please find the attached encrypted file. Please remember the password entered. You wont be able to decrypt the file without it. Download the attached file and copy to the same directory from where you are running the application. Ensure that dbase.json file is there in that location. "
    msg.attach(MIMEText(body, 'plain'))
    filename = file_name+".aes"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read()) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) #adding the encrypted file to p variable.
    msg.attach(p) # Attaching the encrypted file.
    s = smtplib.SMTP('smtp.gmail.com', 587) #Depending on the mail server, you will have to change this. 587 is the port number for smtp.gmail.com
    s.starttls()
    s.login('sender_mail_id', "Application_Password") #For Gmail Users, this has to be generated seperately after enabling 2FA.
    text = msg.as_string()
    s.sendmail('sender_mail_id', toaddress, text) 
    s.quit()

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
def encrypt(message, key, key_size=64):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)
    return dec

# function to generate OTP 
def generateOTP() : 
  
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = "" 

   # length of password can be chaged by changing value in range 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
        
    padding = 4
    OTP.zfill(padding)
    return OTP
# Driver code 
if __name__ == "__main__" : 
    bufferSize = 64 * 1024
    d = {}
    with open('dbase.json', 'r') as f: #This is the pre existing database file of all the old encryptions done using this program.
        d = json.load(f)
    print(d)

    print("What would you like to do? Encrypt/Decrypt?")
    print("Enter 1 for Encrypting your file.")
    print("Enter 2 for Decrypting your file.")
    choice = int(input("Enter your choice: "))
    if (choice == 1):
        print("Welcome. Follow the steps to encrypt your file : ")
        e_file_name = input("Enter the file name you want to encrypt : ")
        password = input("Enter an alphanumeric password for your encryption : ")
        email_ID = input("Enter the owner's email ID which will be used for decryption later : ")
        d[e_file_name] = email_ID
        json_string = json.dumps(d)
        with open('dbase.json', 'w') as f: #Writing the new encrypted file to the existing database.
            json.dump(d, f)
        with open(e_file_name, "rb") as fIn:
            with open(e_file_name+".aes", "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
                print("Encryption Successfull")
                encryption_mail_send(email_ID,e_file_name)
                print("We have sent the Encryption Details to your mail. Please store it for future. Don't share the mail with anyone. Exiting Application")
                exit()
    if (choice == 2):
        print("Welcome. Follow the steps to decrypt your file : ")
        d_file_name = input("Enter the exact file name which you wish to decrypt : ")
        dd = "decrypted_" + d_file_name
        pp = os.path.abspath(dd)
        with open(dd, 'w') as fp:
            pass
    #encrypt_file(file_name,key)
        if d_file_name in d:
            print("Sending mail to ", d[d_file_name] , "check mail for the OTP and enter : ")
            toaddres = d[d_file_name]
            OTP_S = generateOTP()
            decryption_mail_send(OTP_S,toaddres)
            OTP_R = input("Enter the OTP You received on your mail : ")
            d_file_name = d_file_name + ".aes"
            encFileSize = stat(d_file_name).st_size
            if OTP_S == OTP_R:
                password_r = input("Enter the password used at the time of encryption : ")
                with open(d_file_name, "rb") as fIn:
                    try:
                        with open(dd, "wb") as fOut:
            # decrypt file stream
                            pyAesCrypt.decryptStream(fIn, fOut, password_r, bufferSize, encFileSize)
                            print("You can find your decrypted file in" + pp + "directory." )
                    except ValueError:
        # remove output file on error
                        print("Wrong Password, Exiting Application Now.")
                        remove(dd)
                        exit()
        else:
            print("We were not able to find the entered file in our records. Please restart the application and try again.")
