import smtplib
import time
import imaplib
import email

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "pavankalyan.d16@gmail.com"
FROM_PWD    = "SUrya5412417"
SMTP_SERVER = "imap.gmail.com"


def readmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        lat = latest_email_id
        lat = lat -1
        print latest_email_id   ,first_email_id
        
        for i in range(latest_email_id,lat, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print 'From : ' + email_from + '\n'
                    #print 'Subject : ' + email_subject + '\n'
                    if email_from == 'pavankalyan.d16@gmail.com':
                        print "success"
                    else:
                        print "error"
        print email_subject
        return email_subject
    except Exception, e:
        print str(e)


