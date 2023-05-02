import mysql.connector as m
p=input("Enter the password")
mydatabase=m.connect(host="localhost",user="root",password=p)

print("1: Add Student")
print("2: Delete Student")
print("3: Update Student")
print("4: Show Student")
print("5: Exit")

cursor=mydatabase.cursor()
cursor.execute("create database if not exists studentdb")
cursor.execute("use studentdb")
cursor.execute("create table if not exists studentdetails(Stdid int primary key auto_increment,Name varchar(100),Age int default 0)")

while 1:
    def quary1():
        quary="select Stdid from studentdetails"
        cursor.execute(quary)
        id=[]
        result=cursor.fetchall()
        #print(result)
        for i in result:
            for j in i:
                id.append(j)
        #print(id)
        return [id]

    n=int(input("Enter the funtion you want to execute"))
    match n:
        case 1:
            quary="insert into studentdetails(Name,Age) values(%s,%s)"
            data1=input("Enter Student Name:")
            data2=int(input("Enter Student Age:"))
            cursor.execute(quary,[data1,data2])
            quary2="select Stdid from studentdetails where Name=%s and Age=%s"
            cursor.execute(quary2,[data1,data2])
            id=cursor.fetchall()
            # print(id)
            print("Your Student Id is:",id[0][0])
            mydatabase.commit()
            continue
        case 2:
            quary="delete from studentdetails where Stdid=%s and Name=%s"
            data1=int(input("Enter Student ID Number"))
            data2=input("Enter Student Name:")
            cursor.execute(quary,[data1,data2])
            mydatabase.commit()
            continue
        case 3:
            while 1:
                data1=int(input("Enter Student ID Number"))
                b=quary1()
                # print(b)
                # print(b[0])
                if(data1 in b[0]):
                    data2=input("Enter Student Name:")
                    data3=int(input("Enter Student Age:"))
                    quary="update studentdetails set Name=%s,Age=%s where Stdid=%s"
                    cursor.execute(quary,[data2,data3,data1])
                    mydatabase.commit()
                    break
                
                else:
                    print("Invalid Student id Try Again")
                    continue
        case 4:
            while 1:
                data1=int(input("Enter Student ID Number"))
                b=quary1()
                #print(b)
                if(data1 in b[0]):
                    quary="select * from studentdetails where Stdid=%s"
                    #data2=input("Enter Student Name:")
                    cursor.execute(quary,[data1])
                    top=cursor.fetchall()
                    # print(top)
                    print("Student Id is",top[0][0])
                    print("Student Name is:",top[0][1])
                    print("Student Age is:",top[0][2])
                    break
                else:
                    print("Invalid Student id Try Again")
                    continue
        case 5:
            print("****Thankyou for you time****")
            mydatabase.commit()
            break