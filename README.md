# Automatic mailing program

This is a simple program that allows you to send emails to a list of recipients.

To make it work :
 - Create a file named "recipients.csv" in the same directory as the program. Change the column names to match your needs.
 - Create a file named body.html in the same directory as the program. This file will be the body of your email.
 - Create a attachment.pdf file in the same directory as the program. This file will be the attachment of your email.
 - Create a .env file in the same directory as the program. This file will contain your credentials. The file should look like this :
    ```
    16_DIGIT_PSWD=your_16_digit_password
    MAIL_USERNAME=your_email_adress
    ATTACHMENT_PATH=attachment_path
    RECIPIENTS_PATH=recipients_list_path
    ```
 - Run the program with the command `python3 main.py`