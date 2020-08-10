from os import remove,rename
import pickle
from datetime import datetime

#Emp_No = 0

def Date_Validation(Temp_Join_Date):
	a = 0
	def Month_Valid(Temp_Join_Date):
		global Month, a
		if int(Temp_Join_Date[3:5]) <= 12 and int(Temp_Join_Date[3:5]) > 0:
			Month = Temp_Join_Date[3:5]
		else:
			a = 1 

	def Day_Valid(Temp_Join_Date):
		global a
		if int(Month) in [1,3,5,7,8,10,12] and int(Temp_Join_Date[0:2]) > 0 and int(Temp_Join_Date[0:2]) <= 31:
			Day = Temp_Join_Date[0:2]
		elif int(Month) in [4,6,9,11] and int(Temp_Join_Date[0:2]) > 0 and int(Temp_Join_Date[0:2]) <= 30:
			Day = Temp_Join_Date[0:2]
		elif int(Month) == 2 and int(Temp_Join_Date[0:2]) > 0 and int(Temp_Join_Date[0:2]) <= 28:
			Day  = Temp_Join_Date[0:2]
		else:
			a = 1

	def Year_Valid(Temp_Join_Date):
		global a
		Cur_Date = datetime.now()
		Tup = Cur_Date.timetuple()
		Cur_Year = Tup[0] 
		if len(Temp_Join_Date[6:]) == 4 and int(Temp_Join_Date[6:]) <= int(Cur_Year):
			Year = Temp_Join_Date[6:]
		else:
			a = 1
	Month_Valid(Temp_Join_Date)
	Day_Valid(Temp_Join_Date)
	Year_Valid(Temp_Join_Date)

	return a



def Add_Employee():
	global Emp_No, Max_Days, Initial_Basic
	fout1 = open('Employee.dat','ab')
	fout2 = open ('Monthly.dat', 'ab')
	while True:
		Employee_Data = {'Employee_No' : str(Emp_No + 1)}
		Employee_Data['Employee_Name'] = input('Employee Name:')  
		if Employee_Data['Employee_Name'] == '0':
			break
		else:
			Employee_Data['Sex'] = input('Sex:')            
			while True:
				Temp_Birth_Date = input('Date of Birth:') # 12-12-2002
				Final = Date_Validation(Temp_Birth_Date)
				if Final == 1:
					print('\n\aDate Error')
				else:
					Employee_Data['Date_of_Birth'] = Temp_Birth_Date
					break
			while True:
				Temp_Join_Date = input('Join Date:') # 12-12-2002
				Final = Date_Validation(Temp_Join_Date)
				if Final == 1:
					print('\n\aDate Error')
				else:
					Employee_Data['Join_Date'] = Temp_Join_Date
					break
			Employee_Data['Designation'] = input('Designation:')    
			Employee_Data['Basic_Salary'] = input('Basic Salary:')   
			while True:
				Temp_Phone_Number = input('Phone Number:')
				if len(Temp_Phone_Number) != 8:
					print('\n\aInvalid Phone Number')
				else:
					Employee_Data['Phone_Number'] = Temp_Phone_Number
					break
			while True:
				Temp_Mobile_Number = input('Mobile Number:')
				if len(Temp_Phone_Number) != 8:
					print('\n\aInvalid Phone Number')
				else:
					Employee_Data['Mobile_Number'] = Temp_Mobile_Number
					break  
			Employee_Data['Address'] = input('Address:')
			pickle.dump(Employee_Data, fout1)

			Monthly_Data = {'Employee_No' : str(Emp_No + 1)}
			Monthly_Data['Employee_Name'] = Employee_Data['Employee_Name']  
			Monthly_Data['No_of_Working_Days'] = str(Max_Days)          
			Monthly_Data['Basic_Salary'] = str(Initial_Basic * Max_Days)  
			Monthly_Data['DA'] = str(0.55*int(Employee_Data['Basic_Salary']))
			Monthly_Data['HRA'] = str(0.35*int(Employee_Data['Basic_Salary']))    
			Monthly_Data['Conveyance'] = str(0.15*int(Employee_Data['Basic_Salary']))   
			Monthly_Data['Gross'] = str(int(Employee_Data['Basic_Salary']) + int(Employee_Data['DA']) + int(Employee_Data['HRA']) + int(Employee_Data['Conveyance'])) 
			Monthly_Data['Income_Tax'] = '0'
			Monthly_Data['Loan'] = '0'
			Monthly_Data['Salary_Advance'] = '0'
			Monthly_Data['Net'] = '0'

			pickle.dump(Monthly_Data, fout2)


			print()
	fout1.close()
	fout2.close()

def Deductions():

	global Max_Days
	fout1 = open('Monthly.dat','rb')
	fout2 = open('Temp.dat','ab')
	Employee_no = input('Employee No.:')
	f = 0
	try:
		while True:
			Employee_Data = pickle.load(fout)
			Temp_Data = {

								'Employee_No' : Employee_Data['Employee_No'],
								'Employee_Name' : Employee_Data['Employee_Name'],
								'No_of_Working_Days' : Employee_Data['No_of_Days'],
								'Basic_Salary' : Employee_Data['Basic_Salary'],
								'DA' : Employee_Data['DA'],
								'HRA' : Employee_Data['HRA'],
								'Conveyance' : Employee_Data['Conveyance'],
								'Gross' : Employee_Data['Gross'],
								'Income_Tax' : Employee_Data['Income_Tax'],
								'Loan' : Employee_Data['Loan'],
								'Salary_Advance' : Employee_Data['Salary_Advance'],
								'Net' : Employee_Data['Net'] 
							
							}
			if Employee_Data['Employee_No'] == Employee_no :

				No_of_Leaves = int(input('No. of Leaves:'))
				Temp_Data['Basic_Salary'] = str(Initial_Basic * (Max_Days - No_of_Leaves))
				Temp_Data['DA'] = str(0.55*int(Employee_Data['Basic_Salary']))
				Temp_Data['HRA'] = str(0.35*int(Employee_Data['Basic_Salary']))    
				Temp_Data['Conveyance'] = str(0.15*int(Employee_Data['Basic_Salary']))   
				Temp_Data['Gross'] = str(int(Employee_Data['Basic_Salary']) + int(Employee_Data['DA']) + int(Employee_Data['HRA']) + int(Employee_Data['Conveyance']))
				Temp_Data['Income_Tax'] = input('Income Tax:')
				Temp_Data['Loan'] = input('Loan:')
				Temp_Data['Salary_Advance'] = input('Salary Advance:')
				Temp_Data['Net'] = str(int(Employee_Data['Gross']) - int(Temp_Data['Income_Tax']) - int(Temp_Data['Loan']) - int(Temp_Data['Salary_Advance']))
				f = 1
				pickle.dump(Temp_Data,fout2)

			else:
				pickle.dump(Temp_Data,fout2)
	except:
		fout1.close()
		fout2.close()
		remove('Monthly.dat')
		rename('Temp.dat','Monthly.dat')

	if f == 0:
		print('\n\aDirectory Does Not Exist....')

def Update_Employee():

	fout1 = open('Employee.dat','rb')
	fout2 = open('Temp.dat','ab')
	Employee_no = input('Employee No.:')
	f = 0
	try:
		while True:
			Employee_Data = pickle.load(fout)
			Temp_Data = {

								'Employee_No' : Employee_Data['Employee_No'],
								'Employee_Name' : Employee_Data['Employee_Name'],
								'Sex' : Employee_Data['No_of_Days'],
								'Date_of_Birth' : Employee_Data['Basic_Salary'],
								'Join_Date' : Employee_Data['DA'],
								'Designation' : Employee_Data['HRA'],
								'Basic_Salary' : Employee_Data['Conveyance'],
								'Phone_Number' : Employee_Data['Phone_Number'],
								'Mobile_Number' : Employee_Data['Mobile_Number'],
								'Address' : Employee_Data['Address']
							
							}
			if Employee_Data['Employee_No'] == Employee_no :
				print(

					  '1. Sex\n'
					  '2. Date of Birth\n'
					  '3. Join Date\n'
					  '4. Designation\n'
					  '5. Basic Salary\n'
					  '6. Phone Number\n'
					  '7. Mobile Number\n'
					  '8. Address\n'

					  )
				
				c=input('Option:')

				if c in ['1','2','3','4','5','6','7','8']:

					if c == '1':
						Temp_Data['Sex'] = input('Sex:')

					if c == '2':
						Temp_Data['Date_of_Birth'] = input('Date of Birth:')

					if c == '3':
						Temp_Data['Join_Date'] = input('Join Date:')

					if c == '4':
						Temp_Data['Designation'] = input('Designation:')

					if c == '5':
						Temp_Data['Basic_Salary'] = input('Basic Salary:')
						
						Temp1 = open('Monthly.dat','rb')
						Temp2 = open('Temp2.dat','ab')

						try:

							while True:
								Del1_Data = pickle.load(Temp1)
								Del2_Data = {

											'Employee_No' : Del1_Data['Employee_No'],
											'Employee_Name' : Del1_Data['Employee_Name'],
											'No_of_Days' : Del1_Data['No_of_Days'],
											'Basic_Salary' : Del1_Data['Basic_Salary'],
											'DA' : Del1_Data['DA'],
											'HRA' : Del1_Data['HRA'],
											'Conveyance' : Del1_Data['Conveyance'],
											'Gross' : Del1_Data['Gross'],
											'Income_Tax' : Del1_Data['Income_Tax'],
											'Loan' : Del1_Data['Loan'],
											'Salary_Advance' : Del1_Data['Salary_Advance'],
											'Net' : Del1_Data['Net'] 
							
											}
								if Del1_Data['Employee_No'] == Employee_no :
									
									Del2_Data['Basic_Salary'] = Temp_Data['Basic_Salary']
									Del2_Data['DA'] = str(0.55*int(Employee_Data[Basic_Salary]))
									Del2_Data['HRA'] = str(0.35*int(Employee_Data[Basic_Salary]))    
									Del2_Data['Conveyance'] = str(0.15*int(Employee_Data[Basic_Salary]))   
									Del2_Data['Gross'] = str(int(Employee_Data['Basic_Salary']) + int(Employee_Data['DA']) + int(Employee_Data['HRA']) + int(Employee_Data['Conveyance']))
									
									Del2_Data['Net'] = str(int(Employee_Data['Gross']) - int(Temp_Data['Income_Tax']) - int(Temp_Data['Loan']) - int(Temp_Data['Salary_Advance']))
									f = 1
									pickle.dump(Del2_Data,Temp2)

								else:
									pickle.dump(Del2_Data,Temp2)
						except:
							Temp1.close()
							Temp2.close()
							remove('Monthly.dat')
							rename('Temp2.dat','Monthly.dat')


					if c == '6':
						Temp_Data['Phone_Number'] = input('Phone Number:')

					if c == '7':
						Temp_Data['Mobile_Number'] = input('Mobile Number:')

					if c == '8':
						Temp_Data['Address'] = input('Address:')

				
					f = 1
					pickle.dump(Temp_Data,fout2)

			else:
				pickle.dump(Temp_Data,fout2)
	except:
		fout1.close()
		fout2.close()
		remove('Monthly.dat')
		rename('Temp.dat','Monthly.dat')

	if f == 0:
		print('\n\aDirectory Does Not Exist....')

def Employee_Report():
	fout = open('Employee.dat','rb')
	try:
		print('_' * 250)
		print( 'ENo', 'Name' , 'Designation' , 'Sex' , 'Date of Birth' , 'Date of Joining' , 'Basic Salary' , 'Dearness Allowance' , 'HR Allowance' , 'Conveyance' , 'Gross' , 'Net' , sep = '\t')
		print('_' * 250)
		while True:
			Employee_Data = pickle.load(fout)
			print(Employee_Data['Employee_No'] , Employee_Data['Employee_Name'] , Employee_Data['Sex'] , Employee_Data['Date_of_Birth'] , Employee_Data['Date_of_Joining'] , Employee_Data['Designation'] , Employee_Data['Basic_Salary'] , Employee_Data['Phone_Number'] , Employee_Data['Mobile_Nimber'] , Employee_Data['Address'] , sep = '\t')
	except:
		fout.close()
		print('_' * 250)

def Salary_Statement():
	fout = open('Monthly.dat','rb')
	Cur_Date = datetime.now()
	Date_Tuple = Cur_Date.timetuple()
	Salary_Date = 'Date_Tuple[0]' + 'Date_Tuple[1]'
	try:
		print('Salary Statement for the Month of ', Salary_Date)
		print('_' * 250)
		print( 'ENo', 'Name' , 'Designation' , 'Basic Salary' , 'Gross' , 'Deduction' , 'Net' , sep = '\t')
		print('_' * 250)
		while True:
			Employee_Data = pickle.load(fout)
			print(Employee_Data['Employee_No'] , Employee_Data['Employee_Name'] , Employee_Data['Designation'] , Employee_Data['Basic_Salary'] , Employee_Data['Gross'] , Employee_Data['Income_Tax'] + Employee_Data['Salary_Advance'] + Employee_Data['Loan'] , sep = '\t')
	except:
		fout.close()
		print('_' * 250)

def Salary_Slip():
	fout = open('Monthly.dat','rb')
	Cur_Date = datetime.now()
	Date_Tuple = Cur_Date.timetuple()
	Salary_Date = 'Date_Tuple[0]' + 'Date_Tuple[1]'
	Employee_No = input('Employee No.:')
	Employee_Name = input('Employee Name:')
	print('Salary Slip for the Month of ', Salary_Date)
	print('Employee No: ', Employee_No , 'Employee Name: ', Employee_Name), 
	try:
		print('_' * 250)
		while True:
			Employee_Data = pickle.load(fout)
			if Employee_No == Employee_Data['Employee_No']:
				print('Basic         : ', Employee_Data['Basic_Salary'] , '          Deductions:          ', Employee_Data['Income_Tax'] + Employee_Data['Salary_Advance'] + Employee_Data['Loan'] )
				print('DA:          ', Employee_Data['DA'])
				print('HRA:          ', Employee_Data['HRA'])
				print('Conveyance:          ', Employee_Data['Conveyance'])
				print('_' * 250)
				print('Gross Pay:          ', Employee_Data['Gross'], '          Net:          ', Employee_Data['Net'])
	except:
		fout.close()
		print('_' * 250)

Emp_No = 0

Cur_Date = datetime.now()
Date_Tuple = Cur_Date.timetuple()

Mo = int(Date_Tuple[1])

if Mo in [4,6,9,11]:
	Max_Days = 30
elif Mo == 2:
	Max_Days = 28
else:
	Max_Days = 30

Initial_Basic = 1000

while True:
    print('_' * 27 + " MENU " + '_' * 27)
    print("1. Add Employee Details")
    print("2. Add Month End Salary Details")
    print("3. Update Employee Details")
    print("4. Print Employee Report")
    print("5. Print Salary Statement")
    print('6. Print Salary Slip')
    print('0. Exit')
    print()
    ch = input('Enter Option:')
    print()
    if ch in ['1' , '2' ,'3' ,'4' ,'5' ,'6' ,'0']:

        if ch == '1':
        	Add_Employee()
                  
        if ch =='2':
        	Deductions()
                  
        if ch == '3':
        	Update_Employee()
                  
        if ch == '4':
        	Employee_Report()
                  
        if ch == '5':
        	Salary_Statement()
                  
        if ch == '0':
        	Salary_Slip()

    else:
    	print('\n\aOut of Options')
