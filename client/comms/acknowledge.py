"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by Taian Chen

Contains acknowledgement handle function.
"""

from comms import objects, interface

def send_acknowledgement(num_id):
    """
    Sends an acknowledgement byte string.
    Acknowledgments are used generally for confirming authentication and other specific processes (not general data transmission).
    This function is also responsible for relaying failed commands to client interface, and receiving buffer size acknowledgements.
    The latter, buffer size acknowledgements, is to make sure the host knows the length of a transmission that the client is about to send, so it can set its buffer size accordingly.

    Due to the receive function needing to send a buffer size acknowledgement, which would require an endless loop of acknowledgements for each send, acknowledgements are encoded in 4 digit number IDs.
    They are:

    Number ID: 1000
    ID: rca-1.2:connection_acknowledge
    Description: General acknowledgement or confirmation (usually during connect/disconnect).

    Number ID: 1001
    ID: rca-1.2:buffer_size_ok
    Description: Acknowledgement for buffer size messages.

    Number ID: 2000
    ID: rca-1.2:buffer_size_over_spec
    Description: Reply when message length to be sent to the receiver is over 4096 bytes, and exceeds the maximum. This type of failure should never occur, and unless you have a modified client/host, should be reported immediately.

    ###### n/a for sending as client ######
    Number ID: 2001
    ID: rca-1.2:authentication_invalid
    Description: Authentication was invalid, and was rejected by host. Check comms.cfg on both sides to make sure authentication matches.
    ###### n/a for sending as client ######

    ###### n/a for sending as client ######
    Number ID: 2002
    ID: rca-1.2:unknown_command
    Description: Command sent to host was not recognized, and was not executed. This type of failure should never occur, and unless you have a modified client/host, should be reported immediately.
    ###### n/a for sending as client ######

    Number ID: 2003
    ID: rca-1.2:buffer_size_invalid
    Description: Not implemented! Reply when message length received is not an integer.

    :param num_id: ID of acknowledgement to be issued.
    :return: none.
    """
    if num_id in [1000, 1001, 2000, 2003]:
        objects.socket_main.sendall(str(num_id).encode(encoding = "ascii", errors = "replace"))
        print("[INFO]: Issued acknowledgement " + '''"''' + objects.acknowledgement_dictionary[num_id] + '''"''' + " or in numeric ID form, " + str(num_id) + ".")
    else:
        print("[FAIL]: Tried to issue invalid acknowledgement. This should not be normal behavior.")
    pass
pass

def receive_acknowledgement():
    """
    Listens for an acknowledgement byte string, returns booleans whether string was received or failed.
    Acknowledgments are used generally for confirming authentication and other specific processes (not general data transmission).
    This function is also responsible for relaying failed commands to client interface, and receiving buffer size acknowledgements.
    The latter, buffer size acknowledgements, is to make sure the host knows the length of a transmission that the client is about to send, so it can set its buffer size accordingly.

    Due to the receive function needing to send a buffer size acknowledgement, which would require an endless loop of acknowledgements for each send, acknowledgements are encoded in 4 digit number IDs.
    They are:

    Number ID: 1000
    ID: rca-1.2:connection_acknowledge
    Description: General acknowledgement or confirmation (usually during connect/disconnect).

    Number ID: 1001
    ID: rca-1.2:buffer_size_ok
    Description: Acknowledgement for buffer size messages.

    Number ID: 2000
    ID: rca-1.2:buffer_size_over_spec
    Description: Reply when message length to be sent to the receiver is over 4096 bytes, and exceeds the maximum. This type of failure should never occur, and unless you have a modified client/host, should be reported immediately.

    Number ID: 2001
    ID: rca-1.2:authentication_invalid
    Description: Authentication was invalid, and was rejected by host. Check comms.cfg on both sides to make sure authentication matches.

    Number ID: 2002
    ID: rca-1.2:unknown_command
    Description: Command sent to host was not recognized, and was not executed. This type of failure should never occur, and unless you have a modified client/host, should be reported immediately.

    Number ID: 2003
    ID: rca-1.2:buffer_size_invalid
    Description: Not implemented! Reply when message length received is not an integer.

    :return: True/False boolean, only returns True when an acknowledgement is successfully received, otherwise returns False for errors.
    """
    try:
        objects.acknowledgement_num_id = int(interface.receive())
    except objects.socket.error as sae:
        print("[FAIL]: Failed to receive acknowledgement. See below for details.")
        print(sae)
        return False
    except ValueError as ve:
        print("[FAIL]: Failed to decode acknowledgement from a byte string. See below for details.")
        print(ve)
        return False
    pass
    try:
        objects.acknowledgement_id = objects.acknowledgement_dictionary[objects.acknowledgement_num_id]
    except KeyError as ke:
        print("[FAIL]: Acknowledgement number ID to alphabetical ID conversion failed! See below for more details.")
        print(ke)
        return False
    pass
    if objects.acknowledgement_id == "rca-1.2:connection_acknowledge":
        print("[INFO]: Received general acknowledgement.") # general acknowledgement
        return True
    elif objects.acknowledgement_id == "rca-1.2:buffer_size_ok":
        print("[INFO]: Received buffer-size acknowledgement.") # buffer size acknowledgement
        return True
    elif objects.acknowledgement_id == "rca-1.2:buffer_size_over_spec":
        print("[FAIL]: Message length exceeded set maximum buffer size (4096 bytes). This should not be normal behavior.") # buffer size over specification warning
        objects.messagebox.showerror("Raspbot RCA: Buffer Size Over Spec", "The message to be sent to the host exceeded the maximum buffer size of 4096 bytes. This should not be normal behavior. \nUnless the script files have been edited, a bug issue should be made.")
        return False
    elif objects.acknowledgement_id == "rca-1.2:authentication_invalid":
        print("[FAIL]: Did not receive an acknowledgement. Authentication was invalid.") # reply that the authentication values sent to the host were invalid
        objects.messagebox.showerror("Raspbot RCA: Auth Invalid", "Authentication sent to host was invalid! Are you sure the auth values are the same on both client/host configurations?")
        return False
    elif objects.acknowledgement_id == "rca-1.2:unknown_command":
        print("[FAIL]: Command unrecognized by host.") # command unrecognized warning
        objects.messagebox.showwarning("Raspbot RCA: Unknown Command", "Command sent to host was not recognized, and was not executed. This should not be normal behavior.")
        return False
    elif objects.acknowledgement_id == "rca-1.2:buffer_size_invalid":
        print("[FAIL]: Buffer size sent was invalid, and integer conversion failed! This should not be normal behavior.") # buffer size invalid
        objects.messagebox.showerror("Raspbot RCA: Buffer Size Invalid", "Buffer size sent to host was not able to be converted into an integer, and is invalid! This should not be normal behavior.")
    else:
        objects.messagebox.showwarning("Raspbot RCA: Bad Acknowledgement", "The host has replied with an invalid acknowledgement ID." + "\n Received: " + str(objects.acknowledgement_num_id))
        print("[FAIL]: Did not receive an acknowledgement. Instead received: ") # invalid acknowledgement warning
        print(str(objects.acknowledgement_num_id))
        return False
    pass
pass