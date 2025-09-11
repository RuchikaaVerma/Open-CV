# import cv2

# # # Load Haar Cascase classifier
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# # #Load image 
# image = cv2.imread("Face sample .png")
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # ## Detect faces
# faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

# #Draw rectangles around detected faces
# for (x, y, w, h) in faces:
#     cv2.rectangle(image, (x,y), (x + w, y + h), (0, 255, 0), 2)
    
# # # Show the image 
# cv2.imshow("Face Detection", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# #Initialize webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     #Detect faces
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    
#     #Draw rectangles around detected faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
        
#     #Display result
#     cv2.imshow("Real-Time Face Detection", frame)
    
#     #Press 'q' to exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
    
# #Release resources
# cap.release()
# cv2.destroyAllWindows()

# # RUN THE FACE DETECTION APP
# print("Choose an option:\n1. Detect faces in an image\n2. Real-time face detection using webcam")
# choice= input("Enter 1 or 2: ")
# if choice == '1':
#     image_path = input("Enter the path to the image file: ")
#     detect_faces_from_image(image_path)
# elif choice == '2':
#     detect_faces_from_webcam()
# else:
#     print("Invalid choice. Please enter 1 or 2.")   