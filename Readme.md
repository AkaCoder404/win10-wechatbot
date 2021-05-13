# Windows 10 Notification for Wechat

Since wechat for windows does not have a notification popup function when a message is recieved, I wanted to create my own.

Using ```ichat``` and ```win10toast```, I explored possibilities on how I could retrieve wechat messages, send wechat messages, and create notification pop functions. I also explored the ```multiprocessing``` library, so that I could create functions that could send automatic messages based on time or time passed while still recieving/returning messages. 


## wechat.py
This is a simple program that signs into wechat and continuously awaits for new messages. For each new message, it uses ```win10toast``` to create a notification popup. For example, 

```python
@itchat.msg_register([TEXT])
def text_reply(msg):
  '''single chat message'''

```
is called when a text message is recieved (not a groupchat). And msg is the object that is sent, it contains information that can be used, such 

```
  msg.FromUserName - id of user that sent the message
  msg.User.NickName - profile name of user that sent the message
  msg.Text - string that is sent
```

It is easy to automate responses by using ```return```, perhaps in the future I could implement a ai chat bot that can automate simple response

## we



