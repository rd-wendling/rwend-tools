#%%
import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging.handlers import BufferingHandler

logger = logging.getLogger()

def set_logging(
    log_console=True,
    console_level='DEBUG',
    log_file=True,
    log_folder='logs',
    log_file_name='log.log',
    file_level='DEBUG',
    log_email=False,
    email_level='DEBUG',
    logger_name=None
):
    if logger_name:
        logger = logging.getLogger(logger_name)
    else:
        logger = logging.getLogger()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger.setLevel('DEBUG')

    if log_file:
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        log_path = os.path.join(log_folder, log_file_name)
        fh = logging.FileHandler(log_path)
        fh.setLevel(file_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if log_console:
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if log_email:
        bh = BufferingSMTPHandler(1_000_000)
        bh.setLevel(email_level)
        logger.addHandler(bh)

    return logger


def send_log_over_email(logger_obj, fromaddr, toaddr, subject, body=''):
    for handler in logger_obj.handlers:
        if isinstance(handler, BufferingSMTPHandler):
            logger.debug('Sending log over email')
            handler.flush(fromaddr, toaddr, subject, body=body)


class BufferingSMTPHandler(BufferingHandler):
    def __init__(self, capacity):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-5s - %(message)s'))

    def flush(self, fromaddr='', toaddrs='', subject='', body=''):
        if len(self.buffer) > 0:
            try:
                if body != '':
                    body += '\n\n'
                body += 'Log Below: \n\n'
                for record in self.buffer:
                    s = self.format(record)
                    body += s + '\n'
                send_email(fromaddr, toaddrs, subject, body)
            except:
                self.handleError(record)

        self.buffer = []



def send_email(fromaddr, toaddr, subject, body, port=587, server='smtp.gmail.com'):
    
    smtp_server = server
    sender_password = os.environ['gmail_app_pwd']

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr

    body = f'{body} \n\n Caution: This email has been automatically generated. Please do not reply to this email.'
    body_html = '<p>' + body.replace('\n', '<br>') + '</p>'
    body_message = MIMEText(body_html, 'html')
    msg.attach(body_message)

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(fromaddr, sender_password)
        server.sendmail(fromaddr, toaddr.split(','), msg.as_string())