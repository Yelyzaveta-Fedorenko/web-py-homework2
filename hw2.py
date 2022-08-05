from abc import abstractmethod, ABC
from collections import UserDict
from datetime import datetime
import pickle

class AbstractAddressBook(ABC):
    @abstractmethod
    def __next__(self):
        pass

class Field:
    def __init__(self, name5):
        self.value = name5

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Name(Field):
    pass


class Phone:
    def __init__(self, phone):
        self._current_phone = phone
        #self.current_phone = phone

    @property
    def value(self):
        if self._current_phone == None and self._current_phone == "":
            self._current_phone = ""
        else:     
            try:
                lll = int(self._current_phone[1:])

                if len(self._current_phone) < 13 and len(self._current_phone)>10 and isinstance(lll, int):
                    return self._current_phone   
                

            except ValueError:
                
                #print(self._current_phone[1:])
                #print("Please give correct phone11")
                self._current_phone = ""
                return self._current_phone 
        

    @value.setter
    def value(self, phone_setter):
      
        if phone_setter != "" :

            try:
                ff = int(phone_setter[1:])
                if len(phone_setter) < 13 and len(phone_setter)>10 and isinstance(ff, int):
                    self._current_phone = phone_setter
            
                ff = int(self._current_phone[1:])
                if len(self._current_phone) < 13 and len(self._current_phone)>10 and isinstance(ff, int):
                    self.current_phone = self._current_phone

            except ValueError:
                print("Please give correct phone12")
                self._current_phone = ""


class Birthday(Field):
    def __init__(self, birthday):            
        self._birthday=birthday
    
    @property
    def value(self):        
        #print(self._birthday)
        if self._birthday != None and self._birthday != "":
            current_time=datetime.now()
            if len (self._birthday) == 10 and int(self._birthday[0:2]) <=31 and int(self._birthday[3:5]) <=12 and int(self._birthday[6:]) <=current_time.year:
                
                return self._birthday
            else:
                print('Please enter correct birthday1')        
                self._birthday=""
            return self._birthday

    @value.setter
    def value(self, birthday):
        if birthday != None and self._birthday != "":
            current_time=datetime.now()
            if len (birthday) == 10 and int(birthday[0:2]) <=31 and int(birthday[3:5]) <=12 and int(birthday[6:]) <=current_time.year:
                
                self._birthday=birthday
            else:
                self._birthday=""
                print('Please enter correct birthday2')
                return self._birthday


class Record:
    birthday=''
    def __init__(self, name4, *args):
        self.name = name4
        self.phones = []
        self.add_phone(*args)
        

    def add_phone(self, *args) -> None:                
        for item in args:               
               
                if item.value != '' and isinstance (item, Phone):      
                    self.phones.append(item)
  
    def add_birthday(self, birthday) -> None:
        if birthday.value != '' and isinstance (birthday, Birthday):
            self.birthday=birthday


    def delete_phone(self, index) -> str:
        try:
            phone = self.phones.pop(index)
        except IndexError:
            return f"Sorry, there is no phone number with the index {index}"
        return f"phone {phone} deleted from contact {self.name}"
  

    def edit_phone(self, index, phone: Phone) -> str:
        try:
            self.phones[index] = phone
        except IndexError:
            return f"Sorry, there is no phone number to change with the index {index}"
        return f"""Phone with index {index} in record with name {self.name} changed on phone {phone}"""

    def __str__(self) -> str:
        if self.birthday != "00.00.0000":
            return f"Name: {self.name}, phones : {', '.join([str(p) for p in self.phones])}, birthday is {self.birthday}"
        else: return f"Name: {self.name}, phones : {', '.join([str(p) for p in self.phones])}"

    def __repr__(self) -> str:
        return f"Name: {self.name}, phones : {', '.join([str(p) for p in self.phones])}, birthday {self.birthday}"

    def days_to_birthday (self)-> None:
        current_time=datetime.now()
        
        happy_birthday=datetime(year=current_time.year, month=int(self.birthday.value[3:5]), day=int(self.birthday.value[0:2]))
        if happy_birthday.month > current_time.month and happy_birthday.day > current_time.day:                   
            days_to_birthday = happy_birthday - current_time
            a=days_to_birthday.days
        else:
            days_to_birthday = happy_birthday - current_time
            a=days_to_birthday.days+365
                      
        return print(f'{a} days left for { self.name} birthday')


class AddressBook(UserDict, AbstractAddressBook):
    index=0
    filename = "DZ12.bin"

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            content = pickle.load(file)
            #print(content)
        return content


    def add_record(self, obj):
        
        if isinstance(obj, Record):
            if obj.name.value in self.data.keys():
               
                self.data.update({obj.name.value: obj})
            else:
                self.data[obj.name.value] = obj  # , print("bbb")

    def del_record(self, obj):
        del self.data[obj.name.value]

    def delete_record(self, name: Name):
        print( f"Record with name {name} deleted from AddressBook")
        self.data.pop(name)
        

    def __str__(self) -> str:
        result = "\n".join([str(rec) for rec in self.data.values()])
        
        return result

    def __iter__ (self):          
        self.a=[]
        self.data.update(self.read_from_file().data)
        for i in self.data.values():
            self.a.append(i) 
        #d=self.read_from_file()
        #for j in d.data.values():
            #self.a.append(j)   

        return self

    def __next__(self): 
                
        if len(self.a) > self.index: 
            #print(len(self.a))
            c=""           
            c=self.a[self.index] 
            self.index+=1
            
            #print(self.index) 
            
            
            return f"Name: {c.name}, phones : {', '.join([str(p.value) for p in c.phones])} birthday is {c.birthday}"
            
        elif len(self.a) <= self.index: 
            print ('Adress book is ended')
            self.index=0  

def input_error(get_handler):
    def inner(command1):
        try:
            get_handler(command1)
            return get_handler(command1)
        except ValueError as e:
            print(e)
            command1 = "help"
        except IndexError as e:
            print(e)
            command1 = "help"
        except TypeError as e:
            print(e)
            command1 = "help"
        except KeyError as e:
            print("hhhhhh")
            command1 = "help"
        return command1

    return inner


def input_():
    while True:
        user_command1 = input("Please, give me a command:")
        if (
            "hello" in user_command1
            or "exit" in user_command1
            or "close" in user_command1
            or "good bye" in user_command1
            or "show all" in user_command1
            or "phone" in user_command1
            or "add" in user_command1
            or "change" in user_command1
            or "add_phone" in user_command1
            or "del_phone" in user_command1
            or "edit_phone" in user_command1
            or "del_contact" in user_command1
            or "add_birthday" in user_command1
            or "birthday" in user_command1
            or "find"  in user_command1 
                     
        ):
            return user_command1
        continue


def normalization(user_command1):
    user_command1.casefold()
    user_command1_norm = user_command1
    return user_command1_norm


def input_error_2(parser):
    def inner(user_command1_norm):
        a = 0
        while a < 10:
            try:
                name, phone, command1, new_phone, birthday = parser(user_command1_norm)
                a += 1
                return name, phone, command1, new_phone, birthday
            except TypeError:
                print("Give me name and phone please")

            except IndexError:

                print("Give me true name or phone please2")

                while True:
                    user_command1 = input_()
                    user_command1_norm = normalization(user_command1)
                    try:
                        name, phone, command1, new_phone, birthday = parser(user_command1_norm)
                        a += 1
                        return name, phone, command1, new_phone, birthday
                    except:
                        print(f'"{phone}" is not a number. Try again')

            except ValueError:
                print("Give me true name or phone please3")

            except KeyError:
                print("Give me true name or phone please4")

    return inner


def help_func():
    user_command1 = input("Please, give me a new command1:")
    user_command1_norm = normalization(user_command1)
    name, phone, command1, new_phone, birthday = parser(user_command1_norm)
    return name, phone, command1, new_phone, birthday


@input_error_2
def parser(user_command1_norm):
    if user_command1_norm in ["hello", "exit", "close", "good bye", "show all"]:
        command1 = user_command1_norm
        return "", "", command1, "", ""

    elif "add_phone" in user_command1_norm:
        c = user_command1_norm.split(" ")
        
        name = c[1]
        command1 = c[0]
        if len(c) <= 2:
            phone = "no"
        else:
            phone = c[2]

        return name, phone, command1, "", ""

    elif "del_contact" in user_command1_norm:
        c = user_command1_norm.split(" ")
        
        name = c[1]
        command1 = c[0]
        if len(c) <= 2:
            phone = "no"
        else:
            phone = c[2]

        return name, phone, command1, "", "" 


    elif "del_phone" in user_command1_norm:
        c = user_command1_norm.split(" ")
        
        name = c[1]
        command1 = c[0]
        if len(c) <= 2:
            phone = "no"
        else:
            phone = c[2]

        return name, phone, command1, "", ""    


    elif "edit_phone" in user_command1_norm:
        c = user_command1_norm.split(" ")
        
        name = c[1]
        command1 = c[0]
        if len(c) <= 2:
            phone = "no"
        else:
            phone = c[2]
        
            new_phone = c[3]           

        return name, phone, command1, new_phone, ""                    
   
    elif "phone" in user_command1_norm:
        b = user_command1_norm.split("phone ")
        name = b[-1]
        command1 = "phone"
        return name, "", command1, "", ""    
  
    elif "add_birthday" in user_command1_norm:
        c = user_command1_norm.split(" ")
        name = c[1]
        command1 = c[0]
        birthday = c[2]
        """if len(c[2]) < 10:
            birthday = "no"
        else:
           birthday = c[2]"""
           #print(birthday)
           #print(c[2])
        return name, "", command1, "", birthday

    elif "add" in user_command1_norm or "change" in user_command1_norm:
        c = user_command1_norm.split(" ")
        name = c[1]
        command1 = c[0]
        if len(c) <= 2:
            phone = "no"
        else:
            phone = c[2]
        return name, phone, command1, "", ""

    elif "birthday" in user_command1_norm:
        c = user_command1_norm.split(" ")
        name = c[1]
        command1 = c[0]
        #print(name)
        #print(command1)
        
        
        return name, "", command1, "", ''

    elif "find" in user_command1_norm:
        c = user_command1_norm.split(" ")
        name = c[1]
        command1 = c[0]
        #print(name)
        #print(command1)
        
        
        return name, "", command1, "", ''
        
    else:
        name = ""
        phone = ""
        command1 = "help"
        new_phone = ""
        return name, phone, command1, new_phone, birthday

def main():
    def close_func():
        print("Good bye!")

    def show_func(N=2):
        for i in range (0, N):           
           print(next(iter(c_b)))

    def phone_func():
        if name in c_b.data.keys():
            jjj=[]
            for i in c_b.get(name).phones:
                jjj.append(i.value)
                #print(len(c_b.get(name).phones))
                print(f"Name is {name}, phone is {jjj} ")

    def add_func():
        if name in c_b.data.keys():
            phone1.value=phone
            add_phone_func()
        else:                        
            phone1.value=phone
            c_b.add_record(record)

    def del_contact_func():     
        c_b.delete_record(name)
           

    def hello_func():
        print("How can I help you?")

    def add_phone_func():
        record=c_b.data.get(name)
        phone1.value=phone
        #record.current_phone =phone
        record.add_phone(phone1)
        c_b.add_record(record)

    def del_phone_func():
        record=c_b.data.get(name)        
        for i, j in enumerate(record.phones):                       
            if phone == str(j) and j != None:                  
                record.delete_phone(i)
                c_b.add_record(record)

    def edit_phone_func():
        record=c_b.data.get(name)
        phone1.value=new_phone
        #record.new_phone = new_phone
        for i, j in enumerate(record.phones):                       
            if phone == str(j) and j != None:                  
                record.edit_phone(i, phone1)
                
                c_b.add_record(record)       

    def add_birthday_func():

        if name in c_b.data.keys():
            record=c_b.data.get(name)
            birthday1=Birthday(birthday)
            #birthday1.value = birthday
            record.add_birthday(birthday1)
        else: print("Name is absent")

    def birthday_func():
        if name in c_b.data.keys() and c_b.get(name).birthday != '00.00.0000':
            print(c_b.get(name).birthday) 
            record=c_b.data.get(name)
            record.days_to_birthday()

    def find_func():             
        #print(name)
        #print(c_b.data.items())
        if name in str(c_b.data.items()):          

            for k,v in c_b.data.items():
                for i in v.phones:               
                    if name in k or str(name) in i.value:                    
                        print(f"Name is {k}, phonea is {c_b.get(k).phones}")                 
           
        else: print(f"no current Names and phones {name}")
    command1S = {
        "good bye": close_func,
        "close": close_func,
        "exit": close_func,
        "show all": show_func,
        "phone": phone_func,
        "change": add_func,        
        "add_phone": add_phone_func,
        "del_phone": del_phone_func,
        "hello": hello_func,
        "edit_phone": edit_phone_func,
        "help": help_func,
        "del_contact": del_contact_func,
        "add_birthday": add_birthday_func,
        "birthday": birthday_func,
        "add": add_func,
        "find": find_func,
    }

    @input_error
    def get_handler(command1):
        return command1S[command1]

    
    c_b = AddressBook()
    while True:
        try:
            c_b=c_b.read_from_file()            
        except EOFError: 
            c_b = AddressBook()
        except FileNotFoundError:
            c_b = AddressBook()
        #print(type(c_b))
        user_command1 = input_()

        if user_command1 in ["close", "good bye", "exit"]:
            close_func()
            break

        user_command1_norm = normalization(user_command1)

        name, phone, command1, new_phone, birthday = parser(user_command1_norm)

        if command1 != "find":
            name1 = Name(name)
            # name1.value = name
            phone1 = Phone(phone)
            # phone1.phone = phone
            birthday1= Birthday(birthday)
            record = Record(name1, phone1, birthday1)

        #elif command1 == "add_birthday":
            #birthday1= Birthday(birthday)        
            #record = Record(name1, birthday1)    

        if command1 is not None:

            a = get_handler(command1)
            a()
            #paginator = iter(c_b)
        c_b.save_to_file()
if __name__ == "__main__":

    main()
