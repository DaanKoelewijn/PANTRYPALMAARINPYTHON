import mysql.connector
import tkinter as tk
from tkinter import simpledialog

selected_user = None

def retrieve_item_by_ean():
    ean_code = ean_entry.get()
    output_text.delete(1.0, tk.END)

    try:
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Wachtwoord',
            'database': 'test'
        }

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT * FROM product WHERE ean_code = %s"

        cursor.execute(query, (ean_code,))
        item = cursor.fetchone()

        if item:
            output_text.insert(tk.END, "Item Found:\n")
            for index, value in enumerate(item):
                output_text.insert(tk.END, f"{cursor.column_names[index]}: {value}\n")
        else:
            output_text.insert(tk.END, f"Item not found for EAN: {ean_code}\n")

    except mysql.connector.Error as e:
        output_text.insert(tk.END, f"Error connecting to MySQL: {e}\n")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def add_to_nutrition_week():
    global selected_user
    ean_code = ean_entry.get()
    output_text.delete(1.0, tk.END)

    if not selected_user:
        output_text.insert(tk.END, "Please select a user first.\n")
        return

    try:
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Wachtwoord',
            'database': 'test'
        }

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT `Energie in kcal` FROM product WHERE ean_code = %s"
        cursor.execute(query, (ean_code,))
        item = cursor.fetchone()

        if item:
            kcal_value = item[0]

            update_query = "UPDATE user SET `kcal week` = `kcal week` + %s WHERE Naam = %s"
            cursor.execute(update_query, (kcal_value, selected_user))
            conn.commit()

            output_text.insert(tk.END, f"nutritional value added to {selected_user} consumed foods n shit'\n")
        else:
            output_text.insert(tk.END, f"Item not found for EAN: {ean_code}\n")

    except mysql.connector.Error as e:
        output_text.insert(tk.END, f"Error connecting to MySQL: {e}\n")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
def add_new_user():
    global selected_user
    try:
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Wachtwoord',
            'database': 'test'
        }
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Ask for the user's name via a pop-up dialog box
        inputtedname = simpledialog.askstring("Input", "Enter user's name:")
        
        query = "INSERT INTO `test`.`user` (`Naam`, `kcal week`) VALUES (%s,'0');"
        cursor.execute(query, (inputtedname,))
        conn.commit()
        
        # Display a message to indicate successful addition of the user
        output_text.insert(tk.END, f"New user '{inputtedname}' added.\n")
        
    except mysql.connector.Error as e:
        output_text.insert(tk.END, f"Error connecting to MySQL: {e}\n")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
def delete_user():
    try:
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Wachtwoord',
            'database': 'test'
        }
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "DELETE FROM `test`.`user` WHERE (`Naam` = %s);"
        cursor.execute(query, (selected_user,))
        conn.commit()
        output_text.insert(tk.END, f"User '{selected_user}' deleted.\n")

    except mysql.connector.Error as e:
        output_text.insert(tk.END, f"Error connecting to MySQL: {e}\n")
       
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
        
def refresh_user_list():
    try:
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Wachtwoord',
            'database': 'test'
        }
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT Naam FROM user")
        users = cursor.fetchall()
        user_listbox.delete(0, tk.END)  # Clear existing user list
        for user in users:
            user_listbox.insert(tk.END, user[0])
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()    
root = tk.Tk()
root.title("EAN Code Scanner")

select_user_frame = tk.Frame(root)
select_user_frame.pack()

select_user_label = tk.Label(select_user_frame, text="Select User:")
select_user_label.pack()

user_listbox = tk.Listbox(select_user_frame)
user_listbox.pack()

try:
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Wachtwoord',
        'database': 'test'
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT Naam FROM user")
    users = cursor.fetchall()

    for user in users:
        user_listbox.insert(tk.END, user[0])

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()

select_button = tk.Button(select_user_frame, text="Select User", command=lambda: set_selected_user(user_listbox.get(tk.ACTIVE)))
select_button.pack()

def set_selected_user(user):
    global selected_user
    selected_user = user

ean_frame = tk.Frame(root)
ean_frame.pack()

label = tk.Label(ean_frame, text="Scan the EAN code:")
label.pack()

ean_entry = tk.Entry(ean_frame)
ean_entry.pack()

search_button = tk.Button(ean_frame, text="Search", command=retrieve_item_by_ean)
search_button.pack()

add_button = tk.Button(ean_frame, text="Eat", command=add_to_nutrition_week)
add_button.pack()

add_user_button = tk.Button(root, text="Add New User", command=add_new_user)
add_user_button.pack()

add_delete_button = tk.Button(ean_frame, text="Delete User", command=delete_user)
add_delete_button.pack()

add_refresh_button = tk.Button(ean_frame, text="refresh", command=refresh_user_list)
add_refresh_button.pack()

output_text = tk.Text(root, height=10, width=40)
output_text.pack()

root.mainloop()
