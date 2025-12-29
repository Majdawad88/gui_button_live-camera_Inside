#git clone https://github.com/Majdawad88/gui_button_live-camera_Inside.git
import tkinter as tk
from tkinter import Button, Frame
import cv2
from picamera2 import Picamera2
import threading
import sys
import os

class CameraApp:
    def __init__(self, window):
        # Initialize the main Tkinter window
        self.window = window
        self.window.title("Pi Camera - Integrated View")
        self.window.geometry("800x500")
        
        # Initialize the PiCamera2 object
        self.picam2 = Picamera2()
        # Boolean flag to track if the camera is currently streaming
        self.is_running = False
        
        # --- UI Layout ---
        
        # 1. Sidebar: Create a container on the left for controls
        self.sidebar = Frame(window, width=150, bg='#2c3e50')
        self.sidebar.pack(side="left", fill="y")

        # 2. Toggle Button: Change text and color based on camera state
        self.btn = Button(self.sidebar, text="Start Video", command=self.toggle_camera, 
                          width=12, height=2, bg='green', fg='white', font=('Arial', 10, 'bold'))
        self.btn.pack(pady=20, padx=10)

        # 3. Video Container: Create a black frame on the right to hold the feed
        self.video_frame = Frame(window, bg='black')
        self.video_frame.pack(side="right", expand=True, fill="both")

        # Set a protocol to handle clean exit when the window "X" is clicked
        self.window.protocol("WM_DELETE_WINDOW", self.cleanup)

    def video_loop(self):
        """
        Background function that captures frames and displays them using OpenCV.
        """
        try:
            # Configure camera settings (Format and Resolution)
            config = self.picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
            self.picam2.configure(config)
            self.picam2.start()

            # Initialize an OpenCV window named "IntegratedFeed"
            # WINDOW_NORMAL allows the browser/VNC to capture the window more easily
            cv2.namedWindow("IntegratedFeed", cv2.WINDOW_NORMAL)
            
            while self.is_running:
                # Capture a single frame as a NumPy array
                frame = self.picam2.capture_array()
                
                # Display the captured frame in the OpenCV window
                cv2.imshow("IntegratedFeed", frame)
                
                # Wait 1ms for the window to update; check if 'q' is pressed to exit loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Stop the camera and close OpenCV windows when 'is_running' becomes False
            self.picam2.stop()
            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"Error: {e}")
            self.is_running = False

    def toggle_camera(self):
        """
        Switches the camera on or off when the button is clicked.
        """
        if not self.is_running:
            # START CAMERA
            self.is_running = True
            self.btn.config(text="Stop Video", bg='red')
            # Use a Thread so the GUI doesn't freeze while the video is running
            threading.Thread(target=self.video_loop, daemon=True).start()
        else:
            # STOP CAMERA
            self.is_running = False
            self.btn.config(text="Start Video", bg='green')

    def cleanup(self):
        """
        Ensure resources are released properly before the app closes.
        """
        self.is_running = False
        self.picam2.close()  # Close camera hardware
        cv2.destroyAllWindows() # Close any leftover OpenCV windows
        self.window.destroy() # Close the Tkinter window
        sys.exit(0) # Terminate the script

if __name__ == "__main__":
    # Create the root window and start the application
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
