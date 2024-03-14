import cv2
import face_recognition

def detect(request):

    
    
    # Initialize the camera outside of the loop
    video_capture = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not video_capture.isOpened():
        print("Error: Could not open camera.")
        return

    # Initialize a flag to track if a face has been detected in the current video stream
    face_detected = False
    
    while True:
        ret, frame = video_capture.read()
        
        
        # Find face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        
        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            # Compare detected face with stored face images
            for person in MissingPerson.objects.all():
                print(person.image.path)
                stored_image = face_recognition.load_image_file(person.image.path)
                stored_face_encoding = face_recognition.face_encodings(stored_image)[0]

                # Compare face encodings using a tolerance value
                matches = face_recognition.compare_faces([stored_face_encoding], face_encoding)

                if any(matches):
                    name = person.first_name + " " + person.last_name
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    
                    # Check if a face has already been detected in this video stream
                    if not face_detected:
                        
                        print("Hi " + name + " is found")
                        
                        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
                        subject = 'Missing Person Found'
                        from_email = ''
                        recipientmail = person.email
                        recipient_phone_number = '+91'+str(person.phone_number)
                        # lat = request.GET.get('latitude')
                        # lng = request.GET.get('longitude')

                        # url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}'
                        # response = requests.get(url)
                        # data = response.json()
                        # print(data)
                        # city = data['display_name']

                        if request.method == 'POST':
                            data = json.loads(request.body)
                            latitude = data.get('latitude')
                            longitude = data.get('longitude')
                            # Use latitude and longitude as needed
                            print("Latitude:", latitude)
                            print("Longitude:", longitude)

                            url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}'
                            response = requests.get(url)
                            data = response.json()
                            print(data)
                            city = data['display_name']

                        context = {"first_name":person.first_name,"last_name":person.last_name,
                                    'father_name':person.father_name,"aadhar_number":person.aadhar_number,
                                    "missing_from":person.missing_from,"date_time":current_time,"location": city}

                        html_message = render_to_string('findemail.html',context = context)
                        send_mail(subject,'', from_email, [recipientmail], fail_silently=False, html_message=html_message)
                        face_detected = True  # Set the flag to True to indicate a face has been detected
                        break  # Break the loop once a match is found
                
            # Check if no face was detected in the current frame
            if not face_detected:
                name = "Unknown"
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Camera Feed', frame)

        # Hit 'q' on the keyboard to quit!
        # Check for any key press
        key = cv2.waitKey(1)
        print(key)
        if key==ord(' '):
            break

 
    
    # Release the camera and close OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()
    
    return render(request, "surveillance.html")
