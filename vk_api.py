import argparse
import socket
import ssl
import re
import sys


def request(socket, request):
   socket.send((request + '\n').encode())
   socket.settimeout(1)
   recv_data = ""
   while True:
      try:
         data = socket.recv(65535).decode("cp1251")
      except:
         break
      else:
         recv_data += data
   return recv_data

def prepare_message(dict_data: dict):
   message = dict_data["method"] + " " + dict_data["url"] + f" HTTP/{dict_data['version_http']}\n"
   for header, value in dict_data["headers"].items():
      message += f"{header}: {value}\n"
   message += "\n"
   return message

def get_user_id():
   parser = argparse.ArgumentParser()
   parser.add_argument('--id', type=str, help='id пользователя VK')
   args = parser.parse_args()

   if args.id is not None:
      return args.id
   else:
      print("Введите ID пользователя")
      sys.exit(0)

if __name__ == '__main__':
   user_id = get_user_id()
   HOST_ADDR = 'api.vk.com'
   PORT = 443
   regex_name = '''"first_name":"[a-zA-Z]+"'''
   regex_surname = '''"last_name":"[a-zA-Z]+"'''
   with open("token.txt") as file:
       token = file.readline()
   #da
   ssl_contex = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
   ssl_contex.check_hostname = False
   ssl_contex.verify_mode = ssl.CERT_NONE
   with socket.create_connection((HOST_ADDR, PORT)) as sock:
      with ssl_contex.wrap_socket(sock, server_hostname=HOST_ADDR) as client:
         message = prepare_message(
            {
               "method": "GET",
               "url": f"/method/friends.get?user_id={user_id}&fields=nickname&access_token={token}&v=5.131",
               "version_http": "1.1",
               "headers": {"HOST": HOST_ADDR},
               "body": None
            }
         )
         answer = request(client, message).split('\n')[-1]
         names = re.findall(regex_name, answer)
         surnames = re.findall(regex_surname, answer)

         for i in range(len(names)):
            print(names[i].split('''"''')[-2] + " " + surnames[i].split('''"''')[-2])

