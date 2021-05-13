# multi process running main wechat while running automatic message sending, 
# automatic sending can be manipulated to do anything, i.e good morning texts, daily news updates

import time
from multiprocessing import Process, Manager, Value

import itchat
from itchat.content import *
from win10toast import ToastNotifier
from auto_message import morning_message_to

# from nntplib import name
global_my_user_id = ""
global_my_user_name = ""

toaster = ToastNotifier()
while toaster.notification_active():
    time.sleep(0.1)


def print_message(sender, reciever, type, content):
  if type == "Text":
    print(sender, "to", reciever, "|", content)

def window_notif(sender, notification):
  global toaster
  toaster.show_toast(sender, notification, threaded=True, icon_path="wechat_icon.ico", duration=3)  # 3 seconds

# single chat text
@itchat.msg_register([TEXT])
def text_reply(msg):
  global global_my_user_id, global_my_user_name
  '''text messages'''
  # print(msg)  
 
  send_user_id = msg.FromUserName
  recieve_user_id = msg.ToUserName

  # send message to myself
  if send_user_id == recieve_user_id:
    print_message(my_user_name, my_user_name, msg.Type, msg.Text)
    return


  # recieve / send notifications
  if send_user_id == global_my_user_id: # no notifications if I send
    try: 
      print_message(global_my_user_name, msg.User.RemarkName, msg.Type, msg.Text)
    except:
      print_message(global_my_user_name, msg.User.UserName, msg.Type, msg.Text)
    return
  else: 
    try: 
      print_message(msg.User.RemarkName, global_my_user_name, msg.Type, msg.Text)
      window_notif(msg.User.RemarkName, msg.Text)
    except:
      print_message(msg.User.UserName, global_my_user_name, msg.Type, msg.Text)
      window_notif(msg.User.UserName, msg.Text)

# groupchat messages
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
  '''group chats'''
  global global_my_user_id, global_my_user_name

  from_user_nickname = ""
  from_user_id = msg.FromUserName
  chatroom_members = msg.User.MemberList
  
  for chatroom_member in chatroom_members:
    if chatroom_member.UserName == from_user_id:
      from_user_nickname = chatroom_member.NickName
    # print(chat_room_member, "\n")

  print_message(from_user_nickname, msg.User.NickName, msg.Type, msg.Text)  
  if from_user_id is not global_my_user_id:
    window_notif(msg.User.NickName + "/" + from_user_nickname, msg.Text)

  # print(msg.User.NickName, user_nickname, msg.Text)

def itchat_main(my_user_id, my_user_name):
  '''itchat'''
  global global_my_user_id, global_my_user_name
  # global my_user_id, my_user_name
  itchat.auto_login(hotReload=True)

  # search own user information
  my_info = itchat.search_friends()
  my_user_id.value = my_info.UserName
  my_user_name.value = my_info.NickName
  global_my_user_id = my_info.UserName
  global_my_user_name = my_info.NickName 

  print(my_user_name.value, "has signed in")
  itchat.run()

def auto_message_main(my_user_id, my_user_name):
  print("auto message process start")

  # define to whom and what you are sending
  target_user_name = "filehelper"
  message_content = "hi filehelper"

  try:
    itchat.auto_login(hotReload=True)    
    response = morning_message_to(itchat, message_content, target_user_name)
  except Exception as e:
    print("error at auto_message_main")

def main():
  # manage shared variables between process
  manager = Manager()
  shared_my_user_id = manager.Value(str, "")
  shared_my_user_name = manager.Value(str, "")
  
  p1 = Process(target=itchat_main, args=(shared_my_user_id, shared_my_user_name))
  p1.start()  

  time.sleep(5)
  p2 = Process(target=auto_message_main, args=(shared_my_user_id, shared_my_user_name))
  p2.start()

  time.sleep(5)
  # print(shared_my_user_id.value, shared_my_user_name.value)

if __name__ == "__main__":
  main()
