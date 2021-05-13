# update this function to do automated messages

import time
import datetime

def morning_message_to(itchat, content, user_name):
  while True:   
    dt = datetime.datetime.now()
    hour_time = dt.strftime("%H:%M")
    # send message at 7am
    if hour_time == "07:00":
      itchat.send('content', toUserName='filehelper')
      dt_string = dt.strftime("%d/%m/%Y %H:%M:%S")
      print(dt_string, "|", "send morning message to", user_name)   
  
    time.sleep(30)


