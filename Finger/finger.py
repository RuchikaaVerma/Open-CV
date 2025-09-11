import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to count fingers
def count_fingers(hand_landmarks, hand_label):
    fingers = []
    landmarks = hand_landmarks.landmark

    # Thumb: direction depends on hand label
    if hand_label == "Right":
        fingers.append(landmarks[4].x < landmarks[3].x)
    else:
        fingers.append(landmarks[4].x > landmarks[3].x)

    # Other fingers
    for tip in [8, 12, 16, 20]:
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)

    return fingers.count(True)

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            label = handedness.classification[0].label  # 'Left' or 'Right'
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_count = count_fingers(hand_landmarks, label)
            coords = hand_landmarks.landmark[0]  # Wrist position for text placement
            x = int(coords.x * frame.shape[1])
            y = int(coords.y * frame.shape[0])

            cv2.putText(frame, f"{label} Hand: {finger_count}", (x, y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Finger Counter - Both Hands", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
 