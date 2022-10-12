from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://binitiocl5:Khiddirpore_140993@cluster0.dxtutds.mongodb.net/?retryWrites=true&w=majority")
db = cluster["ComplaintsTracker"]
users = db["Users"]
complaints = db["Complaints"]


app = Flask(__name__)
@app.route("/",methods = ['get','post'])

def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", 'Shri.')
    response = MessagingResponse()
    user = users.find_one({'number': number})

    if bool(user) == False:
        response.message(f"Hi, {number}! Welcome to *Samadhan*.\n Enter:\n1️⃣ for Office Building\n2️⃣ for Residential Quarter\n3️⃣ for Guest House")
        users.insert_one({"number": number, "status": "main", "messages": []})

    elif user["text"] == "#":
        response.message("Welcome to *Samadhan*.\n Enter:\n1️⃣ for Office Building\n2️⃣ for Residential Quarter\n3️⃣ for Guest House")
        users.update_one({"number": number}, {"$set": {"status": "main"}})


    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Please enter the correct response")
            return str(response)
        if option == 1:
            response.message("Enter:\n1️⃣ for IndianOil Bhavan, Dhakuria\n2️⃣ for IBP House\n# to go back to main page")
            users.update_one({"number": number}, {"$set": {"status": "office"}})
        elif option == 2:
            response.message("Enter:\n1️⃣ for Anamika Apartment\n2️⃣ for Anjana Apartment\n3 forDevdoot Tower\n4 for Ellora Apartment\n5 for Golf Link Apartment\n6 for Middleton Court"
                             "\n7 for Neelanjan Apartment\n8 for New Alipore Block G\n9 for Servo Tower Housing Complex\n10 for Shantikunj Apartment \n11 for Sukrit Apartment"
                             "\n12 for Temple Tower\n13 for Ultadanga Housing Complex\n# to go back to main page")
            users.update_one({"number": number}, {"$set": {"status": "residential"}})
        elif option == 3:
            response.message("Enter:\n1️⃣ for Ballygunge SMC\n2️⃣ for Himadri Guest House\n3 for Neelanjan Guest House \n4 for Rajhans Guest House \n5for Ultadanga Guest House\n# to go back to main page")
            users.update_one({"number": number}, {"$set": {"status": "guest"}})
        else:
            response.message("Please enter the proper response")
            return str(response)


    elif user["status"] == "office":
        try:
            option = int(text)
        except:
            response.message("Please enter the correct response")
            return str(response)
        if 1 <= option <= 2:
            response.message("Please mention your complaint in brief\n# to go back to main page")
            users.update_one({"number": number}, {"$set": {"status": "complain"}})
        else:
            response.message("Please enter the proper response")
            return str(response)

    elif user["status"] == "residential":
        try:
            option = int(text)
        except:
            response.message("Please enter the correct response")
            return str(response)
        if 1 <= option <= 13:
            response.message("Please mention your complaint in brief\n# to go back to main page")
            users.update_one({"number": number}, {"$set": {"status": "complain"}})
        else:
            response.message("Please enter the proper response")
            return str(response)

    elif user["status"] == "guest":
        try:
            option = int(text)
        except:
            response.message("Please enter the correct response")
            return str(response)
        if 1 <= option <= 5:
            response.message("Please mention your complaint in brief\n# to go back to main page")
            users.update_one({"number": number}, {"$set": {"status": "complain"}})
        else:
            response.message("Please enter the proper response")
            return str(response)

    elif user["status"] == "complain":
        cd = str(datetime.now().day)
        cmo = str(datetime.now().month)
        cy = str(datetime.now().year)
        ch = str(datetime.now().hour)
        cmi = str(datetime.now().minute)
        cs = str(datetime.now().second)
        comp_id = "ES" + cd + cmo + cy + ch + cmi + cs
        response.message(f"Your complaint has been registered with complaint ID {comp_id}")
        complaints.insert_one({"number": number, "cid": comp_id, "text": text, "comp_time": datetime.now()})
        users.update_one({"number": number}, {"$set": {"status": "complained"}})

    elif user["status"] == "complained":
        response.message("Welcome to *Samadhan*.\n Enter:\n1️⃣ for Office Building\n2️⃣ for Residential Quarter\n3️⃣ for Guest House")
        users.update_one({"number": number}, {"$set": {"status": "main"}})

    else:
        response.message("Invalid Response")
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(response)

if __name__ == "__main__":
    app.run()
