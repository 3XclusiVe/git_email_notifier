import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def git(command):
    command_to_execute = str.split(command)
    output = subprocess.check_output(["git"] + command_to_execute)
    return output


def new_version_was_realesed():
    list_of_head_tags = git("tag -l --points-at HEAD")
    list_of_head_tags = str.splitlines(list_of_head_tags)
    new_version_tag_prefix = "v"


    for tag in list_of_head_tags:
        if(tag.startswith(new_version_tag_prefix)):
            return True

    return False

class sender(object):
     pass


def create_notification_message():
    message = MIMEMultipart()
    message['Subject'] = "[new version released]"

    repository_url = git("config --get remote.origin.url")
    repository_url = repository_url[:-5]

    list_of_head_tags = git("tag -l --points-at HEAD")
    list_of_head_tags = str.splitlines(list_of_head_tags)
    new_version_tag_prefix = "v"


    for tag in list_of_head_tags:
        if (tag.startswith(new_version_tag_prefix)):
            new_version = tag

    firmware_url = repository_url + "/" + "releases/tag/" + new_version

    body = "New version of LXT firmware available at:" \
           "\n" + firmware_url + "\n\n" \
            "*** This is an automatically generated email, please do not reply ***"
    message.attach(MIMEText(body, 'plain'))

    return message.as_string()




def send_notification_email(sender, addressees_list):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender.email, sender.password)

    message = create_notification_message()
    for email_address in addressees_list:
        server.sendmail(sender.email, email_address , message)

    server.quit()



if __name__ == "__main__":

    sender = sender()
    sender.email = "sender@gmail.com"
    sender.password = "pass"

    addressees_list = ["reciever1gmail.com", "reciever1@gmail.com"]

    if(new_version_was_realesed()):
        send_notification_email(sender, addressees_list)
