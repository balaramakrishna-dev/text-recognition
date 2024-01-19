from django.http import HttpResponse, JsonResponse
import re
import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:/users/user/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
def extract_text_from_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to perform OCR on the grayscale image
    text = pytesseract.image_to_string(gray_image)

    return text

def pan_data_extraction(request):
    # image path of the local system
    pan_image_path = 'text_app/images/pan.jpg'

    # calling the function extract_text_from_image to extract text from the image
    pan_text = extract_text_from_image(pan_image_path)
    all_text_list = re.split(r'[\n]', pan_text)
    pan_list = []
    for i in all_text_list:
        if i == '':
            continue
        else:
            pan_list.append(i)

    d = dict()
    # creating pattern for DOB
    dob_pattern = re.compile(r'\b(\d{2}/\d{2}/\d{4})\b')
    for i in range(len(pan_list)):
        if 'Permanent Account Number Card' == pan_list[i]:
            d['permanent_account_number'] = pan_list[i+1]
        if 'father\'s' in pan_list[i].lower() and 'name' in pan_list[i].lower():
            d['father_name'] = pan_list[i+1]
        elif 'name' in pan_list[i].lower():
            d['name'] = pan_list[i+1]
        if dob_pattern.search(pan_list[i]):
            data_match = dob_pattern.search(pan_list[i])
            d['d_o_b'] = data_match.group(1)

    return JsonResponse(d)

def aadhar_data_extraction(request):
    aadhar_image_path = 'text_app/images/balaramaadhar.png'

    # calling the function extract_text_from_image to extract text from the image
    aadhar_text = extract_text_from_image(aadhar_image_path)
    aadhar_list = aadhar_text.split("\n")       # Converting the data into list based on new line

    # removing unwanted spaces in the list
    while '' in aadhar_list:
        aadhar_list.remove('')

    # Creating patterns to find number and DOB
    number_pattern = r'^[0-9]{4}\s[0-9]{4}\s[0-9]{4}$'
    dob_pattern = re.compile(r'\b(\d{2}/\d{2}/\d{4})\b')

    d = dict()
    for i in range(len(aadhar_list)):
        if re.match(number_pattern, aadhar_list[i]):
            d['aadhar_number'] = aadhar_list[i]
        if dob_pattern.search(aadhar_list[i]):
            date_match = dob_pattern.search(aadhar_list[i])
            d['d_o_b'] = date_match.group(1)
            d['name'] = aadhar_list[i-1]
        if 'mal' in aadhar_list[i].lower() or 'male' in aadhar_list[i].lower():
            d['gender'] = 'Male'
        if 'female' in aadhar_list[i].lower() or 'fema' in aadhar_list[i].lower():
            d['gender'] = 'Female'

    return JsonResponse(d)
