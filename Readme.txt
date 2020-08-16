You can find the modules required for this program to run in 'requirements.txt' Install the packages first and then proceed with below changes.
Changes to be made in the file before running it :
1 . Whereever it is mentioned 'sender_mail_id', type in your mail ID or the test mail if you have created one.
2 . If you are using GMAIL to send mails, then you can go ahead with the same smtp configuration.
In case of others, find their SMTP Servers and ports used and update in the line where it says 'smtp.gmail.com'
3. If you are using Gmail, you will either have to create an app password. # Generate an app password you have generated from Google. Visit 'https://bit.ly/googleapppasswords' to create one.\
If you already have an app password, you can use the same. And enter the same whereever it says 'Application_Password'
4. While running the code for the first time, ensure that 'dbase.json' is present in the same directory. dbase.json should have one entry as shown in the repository file.

Steps to encrypt and decrypt
1. As of now, I have tested this code for text files only. So to encrypt a new file, create a text file in the same directory. And then follow the steps as mentioned.
2. If you would like to decrypt an encrypted file, ensure that .aes file is present in the directory. Keep your encryption password handy. Without that you cannot access your encrypted file.

Note : If you plan on uploading your script to GitHub or any other location, ensure that you don't mention your sender_mail_id and Application_Password in the file.
If at all you do upload it, those who get access to the repository will be able to send mails using the credentials. 

If you face issues while implementing this code, or sending mails to multiple users, feel free to reach out to me at 'krkolle@gmail.com'