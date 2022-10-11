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
        response.message(f"Hi, {number}! Welcome to *Samadhan*.\n Enter:\n 1️⃣ for Employee\n 2️⃣ for Vendor\n3️⃣ for Administrator")
        users.insert_one({"number": number, "status": "main", "messages": []})

    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Please enter the correct response")
            return str(response)

        if option == 1:
            response.message("Thank you!")
            users.update_one({"number": number}, {"$set": {"status": "Employee"}})
            response.message("Enter:\n 1️⃣ for Office Building\n 2️⃣ for Residential Quarter\n 3️⃣ for Guest House\n 0️⃣ To go back to main menu")

        elif option == 2:
            response.message("Thank you!")
            users.update_one({"number": number}, {"$set": {"status": "Vendor"}})
            response.message("Enter: \n 1️⃣ for List of open complaints \n 2️⃣ for List of last 10 closed complaints\n 3️⃣ for closing open complaints \n0️⃣ To go back to main menu")

        elif option == 3:
            response.message("Thank you!")
            users.update_one({"number": number}, {"$set": {"status": "Administrator"}})
            response.message("Enter: \n 1️⃣ for List of open complaints \n 2️⃣ for List of last 20 closed complaints \n 3️⃣ for Assignment of complaint to vendor\n 0️⃣ To go back to main menu")

        else:
            response.message("Please enter the proper response")
            return str(response)
    elif user["status"] == "Employee":
        try:
            option = int(text)
        except:
            response.message("Please enter the correct response")
            return str(response)

        if 1<= option <= 3:
            response.message("Please mention your complaint in brief alongwith location and room/flat number")
            users.update_one({"number": number}, {"$set": {"status": "complain"}})
        elif option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            response.message("Welcome back to *Samadhan*\n Enter: \n 1️⃣ for Employee \n 2️⃣ for Vendor \n 3️⃣ for Administrator")
        else:
            response.message("Invalid Response")
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
        response.message("Welcome back to *Samadhan*\n Enter: \n 1️⃣ for Employee \n 2️⃣ for Vendor \n 3️⃣ for Administrator")
        users.update_one({"number": number}, {"$set": {"status": "main"}})
    elif user["status"] == "Vendor":
        try:
            option = int(text)
        except:
            response.message("Please enter the correct response")
            return str(response)
        if option == 1:
            response.message("List of open complains is:")
            users.update_one({"number": number}, {"$set": {"status": "ven"}})
        elif option == 2:
            response.message("List of last 10 closed complaints:")
            users.update_one({"number": number}, {"$set": {"status": "ven"}})
        elif option == 3:
            response.message("Select respective complaint for closing")
            users.update_one({"number": number}, {"$set": {"status": "ven"}})
        elif option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            response.message("Welcome back to *Samadhan*\n Enter: \n 1️⃣ for Employee \n 2️⃣ for Vendor \n 3️⃣ for Administrator")
        else:
            response.message("Invalid Response")
    elif user["status"] == "Administrator":
        try:
            option = int(text)
        except:
            response.message("Please enter the correct response")
            return str(response)
        if option == 1:
            response.message("List of open complains is:")
            users.update_one({"number": number}, {"$set": {"status": "admin"}})
        elif option == 2:
            response.message("List of last 20 closed complaints:")
            users.update_one({"number": number}, {"$set": {"status": "admin"}})
        elif option == 3:
            response.message("Select respective complaint for assignment of complaint to vendor")
            users.update_one({"number": number}, {"$set": {"status": "admin"}})
        elif option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            response.message("Welcome back to *Samadhan*\n Enter: \n 1️⃣ for Employee \n 2️⃣ for Vendor \n 3️⃣ for Administrator")
        else:
            response.message("Invalid Response")
    elif user["status"] == "admin":
        response.message("Welcome back to *Samadhan*\n Enter: \n 1️⃣ for Employee \n 2️⃣ for Vendor \n 3️⃣ for Administrator")
        users.update_one({"number": number}, {"$set": {"status": "main"}})
    elif user["status"] == "ven":
        response.message("Welcome back to *Samadhan*\n Enter: \n 1️⃣ for Employee \n 2️⃣ for Vendor \n 3️⃣ for Administrator")
        users.update_one({"number": number}, {"$set": {"status": "main"}})
    else:
        response.message("Invalid Response")
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(response)

if __name__ == "__main__":
    app.run()
