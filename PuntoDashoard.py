import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO

import can
import threading
from TextMessage import TextMessage
from bitarray import bitarray



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Define the CAN ID and button masks
CANID_BODY_BUTTONS = 0x06354000
CANID_BM_TEXT_MESSAGE = 0x0A394021
MASK_BUTTON_VOLUME_UP = 0x8000
MASK_BUTTON_VOLUME_DN = 0x4000
MASK_BUTTON_WINDOWS = 0x0040
MASK_BUTTON_MUTE = 0x2000
MASK_BUTTON_UP = 0x1000
MASK_BUTTON_DOWN = 0x0800
MASK_BUTTON_MENU = 0x0080
MASK_BUTTON_SOURCE = 0x0400
MESSAGE_INSTPANEL_CLEAR = bitarray('0000000000000000')

# Create a CAN bus instance (adjust the interface as needed, e.g., 'can0')
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
latest_message = None

# Initialize TextMessage
text_message = TextMessage(bus)

def receive_can_messages():
    global latest_message
    while True:
        message = bus.recv()
        if message and message.arbitration_id == CANID_BM_TEXT_MESSAGE:
            socketio.emit('new_message', {'message': latest_message})
            decoded_message = text_message.decode([message.data.hex()])
            if decoded_message != latest_message:
                latest_message = decoded_message
                # Clear the screen before displaying the new message
                # bus.send(can.Message(arbitration_id=CANID_BODY_BUTTONS, data=MESSAGE_INSTPANEL_CLEAR.tobytes(), is_extended_id=True))
                # Send the message to the frontend
                socketio.start_background_task(lambda: socketio.emit('new_message', {'message': latest_message}, broadcast=True))
                print(f"Recieved mesg: {latest_message}")

# Start a thread to receive CAN messages
threading.Thread(target=receive_can_messages, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send/<int:button_mask>')
def send_can_message(button_mask):
    msg = can.Message(arbitration_id=CANID_BODY_BUTTONS, data=[(button_mask >> 8) & 0xFF, button_mask & 0xFF], is_extended_id=True)
    bus.send(msg)
    return f"Sent CAN message: {msg}"

@app.route('/test_emit')
def test_emit():
    socketio.emit('new_message', {'message': 'Test Message'}, broadcast=True)
    return "Message emitted"


@socketio.on('connect')
def handle_connect():
    print("Client connected")

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True, allow_unsafe_werkzeug=True)