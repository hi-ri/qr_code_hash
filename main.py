import hashlib
import qrcode
import cv2

def mac_to_hash(mac_address):
    """
    Convert a MAC address into a 5-byte hash code.
    """
    # Generate a SHA-256 hash from the MAC address
    sha256_hash = hashlib.sha256(mac_address.encode('utf-8')).digest()
    
    # Take the first 5 bytes of the hash
    hash_code = sha256_hash[:5]
    return hash_code

def hash_to_qr(hash_code, filename="hash_qr.png"):
    """
    Convert a hash code into a QR code and save it as an image.
    """
    # Convert the hash code into a hex string
    hash_hex = hash_code.hex()
    
    # Create the QR code
    qr = qrcode.QRCode(
        version=1,  # Version 1 means the smallest QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(hash_hex)
    qr.make(fit=True)
    
    # Save the QR code to a file
    img = qr.make_image(fill="black", back_colour="white")
    img.save(filename)
    print(f"QR code saved as {filename}")

def read_qr_from_camera():
    """
    Enable the camera to read a QR code and return the hash code.
    """
    # Initialise the webcam
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    print("Point the camera at the QR code... Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access the camera.")
            break
        
        # Detect and decode the QR code
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            print("QR Code detected!")
            print("Decoded hash code (hex):", data)
            cap.release()
            cv2.destroyAllWindows()
            return bytes.fromhex(data)  # Convert hex string back to bytes
        
        # Display the camera feed
        cv2.imshow("QR Code Scanner", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("No QR code detected.")
    return None

# Example Usage:
if __name__ == "__main__":
    # Step 1: Convert MAC to Hash and Generate QR Code
    mac = "00:1A:2B:3C:4D:5E"  # Replace with your MAC address
    hash_code = mac_to_hash(mac)
    print("5-byte hash code:", hash_code.hex())
    hash_to_qr(hash_code)

    # Step 2: Use Camera to Read QR Code
    detected_hash_code = read_qr_from_camera()
    if detected_hash_code:
        print("Detected 5-byte hash code:", detected_hash_code.hex())
    else:
        print("No hash code detected.")

