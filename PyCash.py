#Import all needed modules

#Datetime, for getting date and modifying it
import datetime as dt
from datetime import timedelta, date

#Matplotlib for graphing
import matplotlib

#Backend of matplotlib to allow use with tkinter
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

#Import figure object 
from matplotlib.figure import Figure

#Import animation function under the name 'animation'
import matplotlib.animation as animation

#import style to change graph's apperance
from matplotlib import style

#Import matplotlib.pyplot under the name 'plt', this will be used to plot data
import matplotlib.pyplot as plt

#Tkinter for creating GUI
import tkinter as tk

#ttk for styling of tkinter elements, like the css of tkinter
from tkinter import ttk

#Pillow to use images
from PIL import Image, ImageTk

#Set variables as global
global co_name
global password

  
#Set variables to defaults
logo_img = "Co_Small.png"
co_name = "Test Name"
acc_balance = 0
invoice_id = 0
exp_invoice_id = 0

#Set variables holding total revenue and expenses to defualt value of 0
total_rev = 0
total_exp = 0

#Text portion of program

#Check if program has been setup before by searching created file for the word "Program Ran"
#Open file in read mode, creating it if it hasn't been created yet, read first line, set to variable
storage_file = open("FEU Program Data.txt", "r")
file_line = storage_file.readline(11)
#Close file
storage_file.close()

#Check if first item in list in file is "Program Ran"
if file_line != "Program Ran":
  #If file doesn't contain the words "Program Ran" that means this is the first run of the program, so run intro code
  
  #Set variables to defaults
  logo_img = "Co_Small.png"
  co_name = "Test Name"
  acc_balance = 0
  
  #Intro
  print("Welcome! Before the program fully launches we need some information from you." + "\n")

  #Get company name
  co_name = input("What is the name of your company? Note: This will also be your username." + "\n")

  #Get password
  password = input("What is your password?" + "\n")
  

  #Give company logo image variable a default value
  logo_img = 0

  #Set loop to true
  loop = True

  #Start loop that checks if loop is true
  while loop:
      #Ask if they have a logo
      logo_given = input("Do you want to upload your company logo for use in the program?" + "\n")
      
      #If user has logo ask for filename and store in variable for future use
      if logo_given == "yes" or logo_given == "Yes":
          logo_img = input("Please type in the filename (including file extension) of the image you wish to use" + "\n")
          #Set loop to false since we recieved valid input and don't need to loop back
          loop = False
          
      #If user doesn't have a logo set image variable to stock photo    
      elif logo_given == "no" or logo_given == "No":
          logo_img = "Co_Small.png"
          #Set loop to false since valid input was recieved
          loop = False

      else:
          #Give error and set loop to true so that code loops back
          print("Sorry, you entered an invalid input, please try again." + "\n")
          loop = True

  #Save values to file

  #Open text file in appending mode
  storage_file = open("FEU Program Data.txt", "a")

  #Create list to store text confirming program ran as well as user entered data
  program_data = ["Program Ran", co_name, logo_img, password]

  #Write list to text file using for loop, each iteration writes an item then enters a new line
  for num in program_data:
      storage_file.write(num+'\n')

  #Close file
  storage_file.close()

#Create empty lists for sales, expenses, dates, and net profit
exp_list = []
sales_list = []
dates_list = []
profit_list= []

#Add 31 zeros to both lists to take up space (graph down below needs values to plot else we get error), fill in 31 zeros because x-axis is equal to list of 31 dates, and both axis must have same number of values
for num in range(1,32):
  exp_list.append(0)
  sales_list.append(0)
  

#Create function to create a sale, takes the paramters customer (customer name) product (product name), quantity, and unit_price
def sell(customer, product, quantity, unit_price):
        #Get global variable invoice id, add one to it
        global invoice_id
        invoice_id = invoice_id + 1
        
        #Make variable total_rev a global variable so that it can be used in the function
        global total_rev
        
        #Calculate amount earned from sale and save to variable, make the variable global
        global sale_rev
        sale_rev = unit_price * quantity
        
        #Add sales revenue to total revenue
        total_rev = total_rev + sale_rev
        
        #Run a for loop 31 times (since 31 items in list) that checks if the (num)th last item in the list is a 0, if it is that means it's a item we can replace, so replace with sale_rev  by indexing list and setting item equal to sale_rev
        for num in range(1,32):
          if sales_list[-num] == 0:
            sales_list[-num] = sale_rev
            #Break loop since value was entered (wouldn't want to enter value of same sale multiple times)
            break 

        #Create loop to calculate and store net profit
        for num in range(0, 31):
          #Index sales and expenses lists to get sales_rev and expense, add them to get net profit (adding since expense saved as a negative number)
          net_profit = sales_list[num] + exp_list[num]
          #Add net profit to profit list
          profit_list[num] = net_profit

        #Assign values of product and customer variables to copy variables, and make the variables global for use outside of function
        global product_copy
        global cus_copy

        product_copy = product
        cus_copy = customer

          
#Create function to create a payment, takes supplier (name of supplier/entity being paid), service being paid for and expense as parameters
def pay(supplier, service, expense):
        #Get global variable expense invoice id, add one to it
        global exp_invoice_id
        exp_invoice_id = exp_invoice_id + 1
        
        #Make variable total_exp a global variable so that it can be used in the function
        global total_exp
        
        #Add expense to total expense
        total_exp = total_exp + expense
        
        #Use same for loop as in sell function, for same purpose (to replace indexes with a value of zero with actual data)
        for num in range(1,32):
          if exp_list[-num] == 0:
            exp_list[-num] = expense
            break
          
        #Create loop to calculate and store net profit
        for num in range(0, 31):
          #Index sales and expenses lists to get sales_rev and expense, add them to get net profit (adding since expense saved as a negative number)
          net_profit = sales_list[num] + exp_list[num]
          #Add net profit to profit list
          profit_list[num] = net_profit

      #Assign values of supplier, service, and expense variables to copy variables, and make the variables global for use outside of function
        global sup_copy
        global serv_copy
        global exp_copy

        sup_copy = supplier
        serv_copy = service
        exp_copy = expense
        
#Create loop to calculate and store previous dates
for num in range(0,31):
    #Get current date, subtract (num) days from it and save to variable 'date'
    date = date.today() - timedelta(num)
    #Append date variable to dates_list
    dates_list.append(date)

#Create loop to calculate and store net profit
for num in range(0, 31):
        #Index sales and expenses lists to get sales_rev and expense, add them to get net profit (adding since expense saved as a negative number)
        net_profit = sales_list[num] + exp_list[num]
        #Add net profit to profit list
        profit_list.append(net_profit)
      
#Begin Creating GUI

#Set font familly and font size for GUI in a variable to be used later
large_font = ("Arial", 12)
#Set future graph's style to 'ggplot', a builtin style of matplotlib
style.use("ggplot")

#Create figure to hold graph
graph_figure = Figure(figsize=(5,5), dpi=100)

#Add subplot to figure
sub_plot = graph_figure.add_subplot(111)

#Set title and axes labels
sub_plot.set_title("Cash Flow")
sub_plot.set_ylabel("Money")
sub_plot.set_xlabel("Date")
        
def animate(i):
  #Erase graph visuals
  sub_plot.clear()

  #Set title and axes labels
  sub_plot.set_title("Cash Flow")
  sub_plot.set_ylabel("Money")
  sub_plot.set_xlabel("Date")
  
  #Replot all data
  sales_plot = sub_plot.bar(dates_list, sales_list, label="Sales", color="green")
  exp_plot = sub_plot.bar(dates_list, exp_list, label="Expenses",color="red")
  net_plot = sub_plot.plot(dates_list, profit_list, label="Net Profit",color="blue")
 
 
#Create function for sale-entering window
def sales_window():
  #Create new window
  top = tk.Toplevel()
  
  #Set title of window
  top.title("Enter A Sale")
  
  #Create frame within new window to hold all future widgets
  sale_enter = tk.Frame(top,bg="green")
  
  #Position frame
  sale_enter.grid(row=0, column=0)
  
  #Create and postion text label that will show categories of data to be entered
  categories = ttk.Label(sale_enter,text="QTY   UNIT PRICE", font=large_font)
  categories.grid(row=1, column=1, padx=5, pady=5)

  #Create and position entry box for customer name, enter default text
  cus_entry = ttk.Entry(sale_enter)
  cus_entry.insert(0, "Enter Customer Name")
  cus_entry.grid(row=1, column=0, padx=5, pady=5)
  
  #Create and postion entry box to be used for product name, enter default text
  product_entry = ttk.Entry(sale_enter)
  product_entry.insert(0, "Enter Product Name")
  product_entry.grid(row=2, column=0, padx=5, pady=5)
  
  #Create and position entry box for quantity of item
  quan_entry = ttk.Entry(sale_enter, width=7)
  quan_entry.insert(0, "0.00")
  quan_entry.grid(row=2, column=1, padx=5, pady=5)

  #Create and position entry box for unit price of item
  price_entry = ttk.Entry(sale_enter, width=7)
  price_entry.insert(0, "0.00")
  price_entry.grid(row=2, column=2, padx=5, pady=5)

  
  #Create and position button to submit data and confrim sale, set command to sell, get values needed to run sell command from entry boxes
  submit = ttk.Button(sale_enter, text="Submit", command=lambda: sell(customer = cus_entry.get(), product = product_entry.get(), quantity = int(quan_entry.get()), unit_price = int(price_entry.get())))
  submit.grid(row=3, column=2, padx=5, pady=5)


#Create function for payment-entering window
def pay_window():
  #Create new window
  top = tk.Toplevel()
  
  #Set title of window
  top.title("Enter A Payment")
  
  #Create frame within new window to hold all future widgets
  pay_enter = tk.Frame(top,bg="red")
  
  #Position frame
  pay_enter.grid(row=0, column=0)

  #Create and position entry box for custom name, enter default text
  sup_entry = ttk.Entry(pay_enter)
  sup_entry.insert(0, "Enter Supplier Name")
  sup_entry.grid(row=1, column=0, padx=5, pady=5)
  
  #Create and postion entry box to be used for name of service paid for, enter default text
  serv_entry = ttk.Entry(pay_enter)
  serv_entry.insert(0, "Enter Service Paid For")
  serv_entry.grid(row=2, column=0, padx=5, pady=5)
 

  #Create and position entry box for expense amount
  exp_entry = ttk.Entry(pay_enter, width=7)
  exp_entry.insert(0, "0.00")
  exp_entry.grid(row=2, column=1, padx=5, pady=5)

  #Create and position button to submit data and confirm payment, set command to pay, get values needed to run pay command from entry boxes
  submit = ttk.Button(pay_enter, text="Submit", command=lambda: pay(supplier = sup_entry.get(), service = serv_entry.get(), expense = int(exp_entry.get()) ))
  submit.grid(row=3, column=3, padx=5, pady=5)
  
  
#Create main class, inherit tkinter class attributes
class FinanceProgram(tk.Tk):
    #Create initialization function, set paramters (self object, arguments, keyword arguments
    def __init__(self, *args, **kwargs) :
        #Create main window by calling on init function
        tk.Tk.__init__(self, *args, **kwargs)
        #Set icon and title of window
        tk.Tk.iconbitmap(self, default="PyCash Logo.ico")
        tk.Tk.wm_title(self, "PyCash")
        #Create frame "container" to take up window space
        container = tk.Frame(self)

        #Fill window with created object
        container.pack(side="top", fill="both", expand = True)
        
        #Configure grid of rows and columns in window; set starting number (0) and priority
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)

        #Create dictionary for frames
        self.frames = { }

        #Create for loop to switch betweeen pages
        for frame_counter in (LoginPage, HomePage, SalesPage, ExpensesPage, GraphPage):

          #Set frame counter as a frame
          frame = frame_counter(container, self)
        
          
          #Add frame counter to frames dictionary
          self.frames[frame_counter] = frame

          #Set grid position of frame, set sticky command to north,south,east,west
          frame.grid(row=0,column=0, sticky="nsew")

        #Call function to show LoginPage
        self.show_frame(LoginPage)

    #Create function to show frame
    def show_frame(self,cont):
        #Get frame from dicitonary and raise using command
        frame = self.frames[cont]
        frame.tkraise()

#Create class for loginpage
class LoginPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    #Create label with text "Login"
    label = tk.Label(self, text="Login", font=large_font)
    label.pack(pady=5, padx=5)

    def submit_info():
      name_entry = name_box.get()
      user_pass = pass_box.get()
      
      if name_entry == co_name and user_pass == password:
        controller.show_frame(HomePage)
        

    #Add profile image
    image = Image.open(logo_img)

    profile_img  = ImageTk.PhotoImage(image)
    profile = tk.Label(self, image=profile_img)
    profile.image = profile_img
    profile.pack(padx=5, pady=5)


    #Create entry box for username
    name_box = ttk.Entry(self)
    name_box.insert(0, "Username")
    name_box.pack(padx=5, pady=5)

    entry_name = name_box.get()
    
    #Create entry box for password
    pass_box = ttk.Entry(self)
    pass_box.insert(0, "Password")
    pass_box.pack(padx=5, pady=5)

    user_pass = pass_box.get()

    #Create button to submit username and password
    submit = ttk.Button(self, text="Submit", command = submit_info)
    submit.pack()


#Create class for home page, inherit tk.Frame
class HomePage(tk.Frame):
    #Create then run initialization function
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        #Create label with text "Home"
        label = tk.Label(self, text="Home", font=large_font)
        #Position label using grid, give padding all around
        label.pack(pady=10, padx=10)

        #Create button to switch to sales page
        button1 = ttk.Button(self, text="Sales",
                command=lambda: controller.show_frame(SalesPage))
        button1.pack(pady=5, padx=5)

        #Create button to switch to expenses page
        button2 = ttk.Button(self, text="Expenses",
                command=lambda: controller.show_frame(ExpensesPage)) 
        button2.pack(pady=5, padx=5)

       #Create button to switch to Analysis page
        button3 = ttk.Button(self, text="Analysis",
                command=lambda: controller.show_frame(GraphPage)) 
        button3.pack(pady=5, padx=5)

         #Create label to show company name
        name_label = tk.Label(self, text=co_name, font=large_font)
        name_label.pack(pady=5, padx=5)

        #Show company logo
        #Open image file
        image = Image.open(logo_img)
        
        #Make image tkinter-compatible
        logo = ImageTk.PhotoImage(image)

        #Create label to hold logo
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo
        logo_label.pack(pady=5, padx=5)
        
       
#Create class for sales window
class SalesPage(tk.Frame):
  #Create then run initialization function
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Sales", font=large_font)
        #Position label using grid, give padding all around
        label.grid(row=0, column=0,  pady=10, padx=10)
                                                      
        #Create button to switch back to home page
        button1 = ttk.Button(self, text="Home",
                command=lambda: controller.show_frame(HomePage)) 
        button1.grid(row=0, column=1, padx=5, pady=5)

        #Create button to switch to expenses page
        button2 = ttk.Button(self, text="Expenses",
                command=lambda: controller.show_frame(ExpensesPage)) 
        button2.grid(row=0, column=2, padx=5, pady=5)


         #Create button to switch to analysis page
        button3 = ttk.Button(self, text="Analysis",
                command=lambda: controller.show_frame(GraphPage)) 
        button3.grid(row=0, column=3, padx=5, pady=5)

        #Create button to open up sale-entering window
        new_window = ttk.Button(self, text="Enter Sale", command=sales_window)
        new_window.grid(row=0, column=4, padx=5, pady=5)

        #Create scrollbar for listbox
        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(row=2, column=5)
        
        #Create and position listbox that will hold sales records, attach scrollbar
        sales_rec = tk.Listbox(self,height=50, width=100, yscrollcommand=scrollbar.set)

        sales_rec.grid(row=2, column=4, padx=5, pady=5)
        scrollbar.config(command=sales_rec.yview)

        #Create command to insert data into listbox
        def insert_list():
          
          #Get current date and store in variable
          current_date = date.today()
          
          #Insert invoice statement to list box
          sales_rec.insert(tk.END, "Invoice #" +str(invoice_id) + "  |  Sold: " + product_copy + "       To: " + cus_copy + "     For: $" + str(sale_rev) + "   |   " + str(current_date))
  
        #Create button to update list with sales info
        update_list = ttk.Button(self, text="Update List", command=insert_list)
        update_list.grid(row=1,column=4)
          
#Create class for expenses window
class ExpensesPage(tk.Frame):
  #Create then run initialization function
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Expenses", font=large_font)
        #Position label using grid, give padding all around
        label.grid(row=0,column=0, pady=10, padx=10)
                                                      
        #Create button to switch back to home page
        button1 = ttk.Button(self, text="Home",
                command=lambda: controller.show_frame(HomePage)) 
        button1.grid(row=0, column=1, padx=5, pady=5)

        #Create button to switch to sales page
        button2 = ttk.Button(self, text="Sales",
                command=lambda: controller.show_frame(SalesPage)) 
        button2.grid(row=0, column=2, padx=5, pady=5)
        

         #Create button to switch to analysis page
        button3= ttk.Button(self, text="Analysis",
                command=lambda: controller.show_frame(GraphPage)) 
        button3.grid(row=0, column=3, padx=5, pady=5)

        #Create button to open up payment-entering window
        new_window = ttk.Button(self, text="Enter Payment", command=pay_window)
        new_window.grid(row=0, column=4, padx=5, pady=5)

         #Create scrollbar for listbox
        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(row=2, column=5)
        
        #Create and position listbox that will hold sales records, attach scrollbar
        pay_rec = tk.Listbox(self,height=50, width=100, yscrollcommand=scrollbar.set)

        pay_rec.grid(row=2, column=4, padx=5, pady=5)
        scrollbar.config(command=pay_rec.yview)
        
      
        #Create command to insert data into listbox
        def insert_payment():
      
          #Get current date and store in variable
          current_date = date.today()
          
          #Insert payment statement to list box
          pay_rec.insert(tk.END, "Invoice #" +str(exp_invoice_id) + "  |  Paid: $" + str(exp_copy) + "       To: " + sup_copy + "     For: " + serv_copy + "   |   " + str(current_date))
  
        #Create button to update list with payment info
        update_list = ttk.Button(self, text="Update List", command=insert_payment)
        update_list.grid(row=1,column=4)
                
#Create class for graph/analyis window
class GraphPage(tk.Frame):
  #Create then run initialization function
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Analysis", font=large_font)
        #Position label using pack, give padding all around
        label.pack(pady=10, padx=10)
                                                      
        #Create button to switch back to home page
        button1 = ttk.Button(self, text="Home",
                command=lambda: controller.show_frame(HomePage)) 
        button1.pack()

         #Create button to switch to sales page
        button2 = ttk.Button(self, text="Sales",
                command=lambda: controller.show_frame(SalesPage)) 
        button2.pack()

        #Create button to switch to expenses page
        button3 = ttk.Button(self, text="Expenses",
                command=lambda: controller.show_frame(ExpensesPage)) 
        button3.pack()

        
        
        #Add sales and expenses bar graphs and net profit line graph as subplots
        sales_plot = sub_plot.bar(dates_list,sales_list, label="Sales", color="green")
        exp_plot = sub_plot.bar(dates_list, exp_list, label="Expenses",color="red")
        net_plot = sub_plot.plot(dates_list, profit_list, label="Net Profit",color="blue")
   
        #Create canvas
        canvas = FigureCanvasTkAgg(graph_figure, self)
      
        #Show canvas
        canvas.show()
        
        #Position graph using pack
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
              
        #Add toolbar and position
        toolbar = NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
#Set program to class
program = FinanceProgram()

#Call animation function, will call animate function on graph_figure after 1 sec per iteration
ani = animation.FuncAnimation(graph_figure, animate, interval=1000)
#Start tkinter mainloop to run code and wait for events
program.mainloop()