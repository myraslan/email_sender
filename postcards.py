import csv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

###
port = 465
email = "email@gmail.com"
password = "password"
###

with open("responses.csv", encoding="utf8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for timestamp, name, txt, postcard in reader:
        print(f"Sending email to {name}. Timestamp: {timestamp}")

        ###
        message = MIMEMultipart()
        message["From"] = "email@gmail.com"
        message["To"] = name
        message["Subject"] = "Happy Valentine's Day!"
        postcard += ".png"
        text="Valentine's Day!"
        ###

        with open(postcard, 'rb') as f:
            # set attachment mime and file name, the image type is png
            mime = MIMEBase('image', 'png', filename = postcard)
            # add required header data:
            mime.add_header('Content-Disposition', 'attachment', filename=postcard)
            mime.add_header('X-Attachment-Id', '0')
            mime.add_header('Content-ID', '<0>')
            # read attachment file content into the MIMEBase object
            mime.set_payload(f.read())
            # encode with base64
            encoders.encode_base64(mime)
            # add MIMEBase object to MIMEMultipart object
            message.attach(mime)

        html = '<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body><p style="font-family: Garamond; text-align: center; margin: 3px; font-size:16px;">Hey!</p>'
        html += '<p style="font-family: Garamond; text-align: center; margin: 3px; font-size:16px;"> You have received <span style="color: rgb(255, 153, 204);">an anonymous message and a cute postcard</span> on ' + text + ' Love and be loved!</p><br>'
        html += '<p style="font-family: Garamond; text-align: center; margin: 0px; font-size:16px;"> <q>' + txt + '</q></p><p style="text-align:center;"><img width="65%" src="cid:0"></p>'
        html+= '<p style="font-family: Garamond; font-size: 16px;">Regards, <br> your MinCult💕</p></body></html>'
        message.attach(MIMEText(html, 'html', 'utf-8'))

        text = message.as_string()
        ###

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(email, password)
            server.sendmail(email, name, text)
