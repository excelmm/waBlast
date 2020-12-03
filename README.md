# WhatsApp Blast Bot
Written in Python, powered by Selenium

## Usage:
- Let the program send a message to the number itself (through a link) - this will open a chat to itself.
- Send the message(s) to be broadcast to the list (an external txt file in the same directory)
- Upon being prompted, enter how many messages to be forwarded.
- Contacts in broadcast list should **only have numeric charactes!** (no letters, symbols or spaces)

## Features:
- Supports all types of forwardable messages, including photos, videos and documents.
- If you need to forward a large file, you must first download it so that it becomes forwardable (before the program asks you how many messages to be forwarded)

## Issues:
- Sometimes stops! (**UNRESOLVED ISSUE**) 
*Whenever I use it, it stops at contact number 2715 - I then need to restart it with a different list (help :3)*
- For now, the number of contacts in the broadcast list should be a multiple of 5 (easily fixed, TODO)