import numpy as np
import cv2
from collections import deque

def setValues(x):
    pass  # Placeholder for trackbar callback

def main():
    # Setup windows and trackbars
    cv2.namedWindow("Color Detector")
    cv2.createTrackbar("Upper Hue", "Color Detector", 153, 180, setValues)
    cv2.createTrackbar("Lower Hue", "Color Detector", 64, 180, setValues)
    cv2.createTrackbar("Upper Saturation", "Color Detector", 255, 255, setValues)
    cv2.createTrackbar("Lower Saturation", "Color Detector", 0, 255, setValues)
    cv2.createTrackbar("Upper Value", "Color Detector", 255, 255, setValues)  # Increased for yellow
    cv2.createTrackbar("Lower Value", "Color Detector", 100, 255, setValues)   # Adjusted for yellow

    # Color buffers and properties
    colors = [(255, 0, 0),    # Blue (BGR)
              (0, 255, 0),    # Green
              (0, 0, 255),    # Red 
              (0, 255, 255)]  # Yellow
    
    # Deques for storing drawing points
    color_points = [deque(maxlen=1024) for _ in range(4)]
    color_index = [0] * 4
    
    kernel = np.ones((5, 5), np.uint8)
    
    # Create paint window
    paintWindow = np.zeros((471, 636, 3)) + 255
    
    # Draw color buttons without gaps
    button_width = 80
    start_x = 40
    
    # Clear button
    paintWindow = cv2.rectangle(paintWindow, (start_x, 0), (start_x + button_width, 65), 
                               (0, 0, 0), 2)
    cv2.putText(paintWindow, "Clear", (start_x + 10, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Color buttons (placed with no gaps)
    start_x += button_width
    for i, color in enumerate(colors):
        paintWindow = cv2.rectangle(paintWindow, (start_x, 0), (start_x + button_width, 65), 
                                   color, -1)
        start_x += button_width

    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get tracker positions
        u_hue = cv2.getTrackbarPos("Upper Hue", "Color Detector")
        l_hue = cv2.getTrackbarPos("Lower Hue", "Color Detector")
        u_sat = cv2.getTrackbarPos("Upper Saturation", "Color Detector")
        l_sat = cv2.getTrackbarPos("Lower Saturation", "Color Detector")
        u_val = cv2.getTrackbarPos("Upper Value", "Color Detector")
        l_val = cv2.getTrackbarPos("Lower Value", "Color Detector")
        
        Upper_hsv = np.array([u_hue, u_sat, u_val])
        Lower_hsv = np.array([l_hue, l_sat, l_val])
        
        # Color detection mask
        mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            
            # Draw circle around detected color
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            
            # Determine which color button was pressed
            if y < 65:  # Within button area
                selected_color = None
                
                # Check which button was pressed
                button_pos = 40
                if button_pos <= x < button_pos + button_width:
                    # Clear button pressed - reset all points
                    color_points = [deque(maxlen=1024) for _ in range(4)]
                
                button_pos += button_width
                for i in range(4):
                    if button_pos <= x < button_pos + button_width:
                        selected_color = i
                        break
                    button_pos += button_width
                
                if selected_color is not None:
                    color_points[selected_color].appendleft((int(x), int(y)))
        
        # Draw all color points on paint window
        paintWindow[:,:,:] = 255  # Reset canvas (except buttons)
        
        # Draw buttons again (they got cleared when we reset canvas)
        button_pos = 40
        
        # Clear button
        paintWindow = cv2.rectangle(paintWindow, (button_pos, 0), (button_pos + button_width, 65), 
                                   (0, 0, 0), 2)
        cv2.putText(paintWindow, "Clear", (button_pos + 10, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Color buttons
        button_pos += button_width
        for i, color in enumerate(colors):
            paintWindow = cv2.rectangle(paintWindow, (button_pos, 0), (button_pos + button_width, 65), 
                                      color, -1)
            button_pos += button_width
        
        # Draw all the points
        for i in range(4):
            points = color_points[i]
            for j in range(1, len(points)):
                if points[j - 1] is None or points[j] is None:
                    continue
                cv2.line(paintWindow, points[j - 1], points[j], colors[i], 5)
        
        cv2.imshow("Camera", frame)
        cv2.imshow("Paint", paintWindow)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
