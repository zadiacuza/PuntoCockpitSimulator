# CAN mesage info for this program
```
CANID_BODY_BUTTONS       = 0x06354000 #
MASK_BUTTON_VOLUME_UP    = ba(hex='0x8000')
MASK_BUTTON_VOLUME_DN    = ba(hex='0x4000')
MASK_BUTTON_WINDOWS      = ba(hex='0x0040')
MASK_BUTTON_MUTE         = ba(hex='0x2000')
MASK_BUTTON_UP           = ba(hex='0x1000')
MASK_BUTTON_DOWN         = ba(hex='0x0800')
MASK_BUTTON_MENU         = ba(hex='0x0080')
MASK_BUTTON_SOURCE       = ba(hex='0x0400')
MESSAGE_INSTPANEL_CLEAR = bitarray('0000000000000000')
``` 

## Send info
When pressing menu the follwing can mesage wil be Send
```
cansend vcan0 06354000#0080
# Or when on loopback without being connected to car"
cansend can0 06354000#0080
```
If PuntoConnect is running is wil respond with a message
In this case it wil send something back to open a menu And show welcome messsage in the little screen

### These are not yet in used
```
MASK_DOOR_DRIVER         = ba(hex='0x0004000000000000')
MASK_DOOR_PASSENGER      = ba(hex='0x0008000000000000')

MASK_ARROW_LEFT          = ba(hex='0x000040000000')
MASK_ARROW_RIGHT         = ba(hex='0x000020000000')
```