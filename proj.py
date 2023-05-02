import mysql.connector
from tabulate import tabulate 
import pandas as pd
import maskpass
import pywhatkit
# Connect to the MySQL database
p=maskpass.advpass()
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password=p
)

# Create the drivers table if it doesn't exist
db_cursor = db.cursor()
db_cursor.execute("create database if not exists driver_db")
db_cursor.execute("use driver_db")
db_cursor.execute("CREATE TABLE IF NOT EXISTS drivers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), phone_number VARCHAR(255) unique key, car_model VARCHAR(255), car_type VARCHAR(255), car_capacity int, city_area VARCHAR(255), car_number VARCHAR(255) unique key, license_number VARCHAR(255), registration_number VARCHAR(255))")
db_cursor.execute("CREATE TABLE IF NOT EXISTS customers (id int auto_increment primary key,customer_name VARCHAR(255),customer_number varchar(10) unique key,Driver_Name VARCHAR(255),Source_Location VARCHAR(255),Destination VARCHAR(255),Car_Number VARCHAR(255))")
# Define the main menu function
print("Welcome to the RR Car Rental Driver Registration System")
print("1: Customer")
print("2: Admin")
cho=int(input("Select the option: "))
match cho:
    case 1:
        print("1: Book a Cab")
        print("2: See your Booking")
        print("3: Cancel Booking")
        print("4: exit")
        cous=int(input("Select the option: "))
        match cous:
            case 1:
                while True:
                    loc=input("Enter the Location: ")
                    print("***Car Types***")
                    print("Hatchback")
                    print("Sedan")
                    print("Premium")
                    type=input("Enter Car Type you want: ").lower()
                    dest=input("Enter destination you want to go: ")
                    query="select name,car_type,car_number from drivers where city_area=%s and car_type=%s"
                    db_cursor.execute(query,[loc,type])
                    rows = db_cursor.fetchall()
                    # Printing the Registered driver information in a tabulated form
                    passInfo = pd.DataFrame(rows, columns=["name","car_type","car_number"]) 
                    if len(passInfo) != 0:
                        print("\n")
                        print(tabulate(passInfo, headers="keys",showindex="never", tablefmt="pretty"))
                        data1=input("Enter the name of the Driver you want to select: ")
                        data2=input("Enter your name: ")
                        data3 = input("Enter your phone number: ")
                        q="select customer_number from customers where customer_number=%s"
                        db_cursor.execute(q,[data3])
                        rows=db_cursor.fetchall()
                        passInfo = pd.DataFrame(rows, columns=["phone_number"])
                        # print(len(passInfo))
                        if data3.isdigit()==True and len(data3)==10 and len(passInfo)==0:
                            pass
                        elif(data3.isdigit()==True and len(data3)==10 and len(passInfo)>=1):
                            print("You cannot Enter duplicate Number")
                            print("Try Again")
                            print("\n")
                            continue
                        else:
                            print("Enter a valid Phone number:")
                            continue
                        query2="select car_number from drivers where city_area=%s and car_type=%s and name=%s"
                        db_cursor.execute(query2,[loc,type,data1])
                        row = db_cursor.fetchone()
                        # print(row[0])
                        num=str(row[0])
                        query1="insert into customers(customer_name,customer_number,Driver_Name,Source_Location,Destination,Car_Number) values(%s,%s,%s,%s,%s,%s)"
                        db_cursor.execute(query1,[data2,data3,data1,loc,dest,num])
                        q1="update drivers set city_area=%s where car_number=%s"
                        db_cursor.execute(q1,[dest,num])
                        db.commit()
                        q2="select id from customers where customer_name=%s and Driver_Name=%s and Source_Location=%s and Destination=%s and Car_Number=%s"
                        db_cursor.execute(q2,[data2,data1,loc,dest,num])
                        row=db_cursor.fetchone()
                        print("Hi", data2, "please note your id ",row[0]," for future use")
                        print("Hi ",data2 ,"your cab from ",loc," to ",dest," has been booked and ",data1," with car number ",num," will contact you soon")
                        data4="+91"+data3
                        pywhatkit.sendwhatmsg_instantly(data4,"Hi ",data2 ,"your cab from ",loc," to ",dest," has been booked and ",data1," with car number ",num," will contact you soon")
                        break   
                    if len(passInfo)==0:
                        print("Sorry No driver in your location with this requirement")
                        print("Try Again")
                        print("\n")
            case 2:
                name=input("Enter your name: ")
                query=("SELECT * FROM customers where customer_name=%s")
                db_cursor.execute(query,[name])
                rows = db_cursor.fetchall()
                # Printing the Registered driver information in a tabulated form
                passInfo = pd.DataFrame(rows, columns=["id","customer_name","customer_number","Driver_Name","Source_Location","Destination","Car_Number"]) 
                if len(passInfo) != 0: 
                    print(tabulate(passInfo, headers="keys",showindex="never", tablefmt="pretty"))
                if len(rows) == 0:
                    print("No customer log registered yet.")
            case 3:
                data3=input("Enter the customer id: ")
                data1=input("Enter your name: ")
                data2=input("Enter Drivers name: ")
                query="delete from customers where customer_name=%s and driver_name=%s and id=%s"
                db_cursor.execute(query,[data1,data2,data3])
                db.commit()
                print("Cancellation Successfull")    
    case 2:
        while True:
            admin=input("Enter Admin ID: ")
            passw=maskpass.advpass()
            if(admin=="" or passw==""):
                print("Feilds cannot be empty")
            elif(admin=="rrcars" and passw=="12345"):
                print("Welcome to RR Car Rental Admin Page")
                while True:
                    print("Please choose an option:")
                    print("1. Register new driver")
                    print("2. View registered drivers")
                    print("3. Update Driver Details")
                    print("4. Delete Driver Details")
                    print("5. Exit")
                    choice = int(input("Enter your choice: "))
                    match choice:
                        case 1:
                            # print("Please enter the following information:")

                            query="INSERT INTO drivers (name, phone_number , car_model, car_type, car_capacity, city_area, car_number, license_number, registration_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            while True:
                                name1=input("Enter First name")
                                name2=input("Enter Last name")
                                if name1.isalpha()==False and name2.isalpha()==False:
                                    print("enter a valid name")
                                    continue
                                else:
                                    name=name1+" "+name2
                                    break
                            
                            while True:
                                phone_number = input("Phone number: ")
                                q="select phone_number from drivers where phone_number=%s"
                                db_cursor.execute(q,[phone_number])
                                rows=db_cursor.fetchall()
                                passInfo = pd.DataFrame(rows, columns=["phone_number"])
                                # print(len(passInfo))
                                if phone_number.isdigit()==True and len(phone_number)==10 and len(passInfo)==0:
                                    break
                                elif(phone_number.isdigit()==True and len(phone_number)==10 and len(passInfo)>=1):
                                    print("You cannot Enter duplicate Number")
                                    print("Try Again")
                                    print("\n")
                                else:
                                    print("Enter a valid Phone number:")
                                    continue
                            while True:
                                car_model = input("Car Model: ")
                                if car_model.isalpha()==False:
                                    print("enter a valid Model")
                                    continue
                                else:
                                    break
                            
                            while True:
                                car_type = input("Car type: ")
                                if car_type.isalpha()==False:
                                    print("Enter a valid Car Type")
                                    continue
                                else:
                                    break
                            
                            while True:
                                car_capacity = input("Car capacity: ")
                                if car_capacity.isdigit()==True and int(car_capacity)<=10 and int(car_capacity)>1:
                                    break
                                else:
                                    print("Enter a valid Capacity")
                                    continue
                            
                            while True:
                                city_area=(input("City: "))
                                if city_area.isalpha()==False:
                                    print("Enter a valid City Name")
                                    continue
                                else:
                                    break
                            
                            while True:
                                car_number = input("Car number(without space): ")
                                q="select car_number from drivers where car_number=%s"
                                db_cursor.execute(q,[car_number])
                                rows=db_cursor.fetchall()
                                passInfo = pd.DataFrame(rows, columns=["car_number"])
                                # print(len(passInfo))
                                if (car_number.isalnum()==True and len(passInfo)==0):
                                    # print("Done")
                                    break
                                elif(car_number.isalnum()==True and len(passInfo)>=1):
                                    print("Car Number cannot be Duplicate")
                                    continue
                                else:
                                    print("Enter a valid car Number")
                                    continue
                            while True:
                                license_number = input("Driving License number: ")
                                if (license_number.isalnum()==False):
                                    print("Enter a valid City Name")
                                    continue
                                else:
                                    break
                            
                            while True:
                                registration_number = input("Registration number: ")
                                if (registration_number.isalnum()==False):
                                    print("Enter a valid City Name")
                                    continue
                                else:
                                    break
                            db_cursor.execute(query,[name, phone_number , car_model, car_type, car_capacity, city_area, car_number, license_number, registration_number])                
                            db.commit()
                            print("Driver registered successfully!")
                        case 2:
                            db_cursor.execute("SELECT * FROM drivers")
                            rows = db_cursor.fetchall()
                            # Printing the Registered driver information in a tabulated form
                            passInfo = pd.DataFrame(rows, columns=["id","name", "phone_number", "car_model", "car_type", "car_capacity", "city_area", "car_number", "license_number", "registration_number"]) 
                            if len(passInfo) != 0:
                                print("\n\n")
                                print(tabulate(passInfo, headers="keys",showindex="never", tablefmt="pretty"))
                            if len(rows) == 0:
                                print("No drivers registered yet.")
                        case 3: 
                            data1=input("Enter what you want to change: ")
                            data3=input("Enter Car Number: ")
                            match data1:
                                case "name":
                                    while True:
                                        name1=input("Enter the First Name: ")
                                        name2=input("Enter the Second Name: ")
                                        
                                        if name1.isalpha()==True and name2.isalpha()==True:
                                            name=name1+" "+name2
                                            query="update drivers set name=%s where car_number=%s"
                                            db_cursor.execute(query,[name,data3])
                                            db.commit()
                                            break
                                        else:
                                            print("print valid Name")
                                            continue
                                case "phone number":
                                    while True:
                                        data2=input("Enter the value: ")
                                        if(data2.isdigit()==True and len(data2)==10):
                                            query="update drivers set phone_number=%s where car_number=%s"
                                            db_cursor.execute(query,[data2,data3])
                                            db.commit()
                                            break
                                        else:
                                            print("Enter a Valid Phone Number")
                                            continue
                                case "car model":
                                    while True:
                                        data2=input("Enter the value: ")
                                        if(data2.isalpha()==True):
                                            query="update drivers set car_model=%s where car_number=%s"
                                            db_cursor.execute(query,[data2,data3])
                                            db.commit()
                                            break
                                        else:
                                            print("Enter valid Car Model")
                                            continue
                                case "car type":
                                    while True:
                                        data2=input("Enter the value: ")
                                        if(data2.isalpha()==True):
                                            query="update drivers set car_type=%s where car_number=%s"
                                            db_cursor.execute(query,[data2,data3])
                                            db.commit()
                                            break
                                        else:
                                            print("Enter Valid Car Type")
                                            continue
                                case "capacity":
                                    while True:
                                        data2=int(input("Enter the value: "))
                                        if(data2<=10 and data2>1):
                                            query="update drivers set car_capacity=%s where car_number=%s"
                                            db_cursor.execute(query,[data2,data3])
                                            db.commit()
                                            break
                                        else:
                                            print("Enter a valid Capacity")
                                            continue
                                case "City":
                                    while True:
                                        data2=input("Enter the value: ")
                                        if(data2.isalpha()==True):
                                            query="update drivers set city_area=%s where car_number=%s"
                                            db_cursor.execute(query,[data2,data3])
                                            db.commit()
                                            break
                                        else:
                                            print("Enter valid City Name")
                                            continue
                                case "Lincese Number":
                                    while True:
                                        data2=input("Enter the value: ")
                                        if(data2.isalnum()==True):
                                            query="update drivers set license_number=%s where car_number=%s"
                                            db_cursor.execute(query,[data2,data3])
                                            db.commit()
                                            break
                                        else:
                                            print("Enter a valid Lincese Number")
                                            continue
                                case "Registration Number":
                                    while True:
                                        data2=input("Enter the value: ")
                                        if(data2.isalnum()==True):
                                            query="update drivers set registration_number=%s where car_number=%s"
                                            db_cursor.execute(query,[data2,data3])
                                            db.commit()
                                            break
                                        else:
                                            print("Enter a Valid Registration Number")
                                            continue
                                case _:
                                    print("Enter Valid Input")
                            print("Update Successful")
                        case 4:
                            db_cursor.execute("SELECT * FROM drivers")
                            rows = db_cursor.fetchall()
                            # Printing the Registered driver information in a tabulated form
                            passInfo = pd.DataFrame(rows, columns=["id","name", "phone_number", "car_model", "car_type", "car_capacity", "city_area", "car_number", "license_number", "registration_number"]) 
                            if len(passInfo) != 0:
                                print("\n\n")
                                print(tabulate(passInfo, headers="keys",showindex="never", tablefmt="pretty"))
                            if len(rows) == 0:
                                print("No drivers registered yet.")
                                
                            data1=input("Enter Driver Name:")
                            data2=input("Enter Car Number")
                            try:
                                
                                query="delete from drivers where name=%s and car_number=%s"
                                db_cursor.execute(query,[data1,data2])
                                print("Driver Successfully Removed")
                                db.commit()
                            except:
                                print("Enter Valid name and Car number!")
                        case 5:
                            print("****Thankyou for Your Time****")
                            exit()
                        case _:
                            print("Invalid Choice")
            else:
                print("Id or Password is Wrong")
                print("Try Again")  