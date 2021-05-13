# single process running wechat.py bot
import time
import itchat
from itchat.content import *
from win10toast import ToastNotifier
from auto_message import morning_message_to

# parallel functions
# automate morning messages but keep recieving notifications
from multiprocessing import Process, Manager, Value

# get personal id on first recieve
my_user_id = ""
my_user_name = ""

# handle notification
toaster = ToastNotifier()
while toaster.notification_active():
    time.sleep(0.1)

def window_notif(sender, notification):
  global toaster
  toaster.show_toast(sender, notification, threaded=True, icon_path="wechat_icon.ico", duration = 5)  # 3 seconds

def print_message(sender, reciever, type, content):
  if type == "Text":
    print(sender, "to", reciever, "|", content)
  else:
    print(sender, "to", reciever, "|", content)

# single chat text messages
@itchat.msg_register([TEXT])
def text_reply(msg):
  '''text messages'''
  # print(msg)
  global my_user_id, my_user_name

  send_user_id = msg.FromUserName
  recieve_user_id = msg.ToUserName

  # send message to myself
  if send_user_id == recieve_user_id:
    print_message(my_user_name, my_user_name, msg.Type, msg.Text)
    return

  # recieve/send notifications 
  if send_user_id == my_user_id: # no notifications if I send
    try: 
      print_message(my_user_name, msg.User.RemarkName, msg.Type, msg.Text)
    except:
      print_message(my_user_name, msg.User.UserName, msg.Type, msg.Text) # filehelper case
  else: 
    try: 
      print_message(msg.User.RemarkName, my_user_name, msg.Type, msg.Text)
      window_notif(msg.User.RemarkName, msg.Text)
    except:
      print_message(msg.User.UserName, my_user_name, msg.Type, msg.Text)
      window_notif(msg.User.UserName, msg.Text)
      

# single chat media messages
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
  '''media messages'''
  global my_user_id, my_user_name

  send_user_id = msg.FromUserName
  recieve_user_id = msg.ToUserName

  if my_user_id == send_user_id:
    print_message(my_user_name, msg.User.NickName, msg.Type, "[{}]".format(msg.Type))
  else:
    print_message(msg.User.NickName, my_user_name, msg.Type, "[{}]".format(msg.Type))
    window_notif(msg.User.NickName, "[{}]".format(msg.Type))
  
# groupchat text messages
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
  '''group chats'''
  global my_user_id, my_user_name

  # from_user_nickname = ""
  # from_user_displayname = ""
  from_user_id = msg.FromUserName
  chatroom_members = msg.User.MemberList

  # print(from_user_id, my_user_id)

  # print(msg.User)
  # print(msg.User.Self)

  # print(from_user_id)
  
  # for chatroom_member in chatroom_members:
  #   print(chatroom_member)
  #   if chatroom_member.UserName == from_user_id:
  #     from_user_nickname = chatroom_member.NickName
  #     from_user_nickname = chatroom_member.DisplayName

  # no information on who sent the message
  # print_message(from_user_nickname, msg.User.NickName, msg.Type, msg.Text)  
  print(msg.User.NickName, "|", msg.Text)
  if from_user_id != my_user_id:
    window_notif(msg.User.NickName, msg.Text)

# groupchat media messages
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def download_files(msg):
  '''group chat media'''
  global my_user_id, my_user_name

  # from_user_nickname = ""
  # from_user_displaname = ""
  from_user_id = msg.FromUserName 
  chatroom_members = msg.User.MemberList

  # print(msg.User)
  # for chatroom_member in chatroom_members:
  #   if chatroom_member.UserName == from_user_id:
  #     from_user_nickname = chatroom_member.NickName
  #   # print(chat_room_member)
  
  # print_message(msg.User.NickName, user_nickname, msg.Type)
  print(msg.User.NickName ,"|", msg.Type)

  if from_user_id != my_user_id:
    window_notif(msg.User.NickName, msg.Type)
  
def search_friend(name):
  friend_info = itchat.search_friends(name=name)
  return friend_info

def itchat_main():
  '''itchat'''
  global my_user_id, my_user_name
  itchat.auto_login(hotReload=True)

  # search own user information
  my_info = itchat.search_friends()
  my_user_id = my_info.UserName
  my_user_name = my_info.NickName

  print(my_user_name, "has signed in")
  itchat.run()

if __name__ == "__main__":
  itchat_main()