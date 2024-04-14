import psycopg2
from psycopg2 import sql
import random

# Establishing a connection to the PostgreSQL database
def connect():
    return psycopg2.connect(
        dbname="projectv2.0",
        user="postgres",
        password="Emmanuel01!",
        host="localhost",
        port="4562"
    )

# Function to create tables for Health and Fitness Club Management System
def create_tables(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Members (
                member_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100),
                birthdate DATE,
                weight FLOAT,
                height FLOAT,
                fitness_goal VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Trainers (
                trainer_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS FitnessGoals (
                goal_id INT PRIMARY KEY NULL,
                member_id INT NOT NULL,
                goal_description TEXT NOT NULL,
                goal_date DATE NOT NULL,
                FOREIGN KEY (member_id) REFERENCES Members(member_id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AdministrativeStaff (
                staff_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Classes (
                class_id SERIAL PRIMARY KEY,
                class_name VARCHAR(100),
                trainer_id INT REFERENCES Trainers(trainer_id),
                max_capacity INT,
                class_time TIMESTAMP,
                duration INTERVAL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ClassBookings (
                booking_id SERIAL PRIMARY KEY,
                member_id INT REFERENCES Members(member_id),
                class_id INT REFERENCES Classes(class_id),
                booking_time TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PersonalTrainingSessions (
                session_id SERIAL PRIMARY KEY,
                member_id INT REFERENCES Members(member_id),
                trainer_id INT REFERENCES Trainers(trainer_id),
                session_time TIMESTAMP,
                duration INTERVAL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Equipment (
                equipment_id SERIAL PRIMARY KEY,
                equipment_name VARCHAR(100),
                purchase_date DATE,
                maintenance_interval INTERVAL,
                last_maintenance_date DATE
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payments (
                payment_id SERIAL PRIMARY KEY,
                member_id INT REFERENCES Members(member_id),
                amount DECIMAL(10, 2),
                payment_time TIMESTAMP
            )
        """)
        connection.commit()
def insert_initial_data(connection):
    with connection.cursor() as cursor:
        classes_data = [
            ('Yoga', 1, 15, '2024-04-15 10:00:00', '1 hour'),
            ('Pilates', 2, 10, '2024-04-16 09:00:00', '45 minutes'),
            ('Spinning', 3, 20, '2024-04-17 18:00:00', '1 hour'),
            ('Zumba', 4, 15, '2024-04-18 17:30:00', '1 hour'),
            ('Bootcamp', 5, 20, '2024-04-19 06:00:00', '1.5 hours')
        ]
        try: 
            for class_data in classes_data:
                cursor.execute("""
                    INSERT INTO Classes (class_name, trainer_id, max_capacity, class_time, duration)
                    VALUES (%s, %s, %s, %s, %s)
                """, class_data)
            print("Data inserted successfully!")
            connection.commit()
        except psycopg2.Error as e:
            print("Error:", e)
# Function to insert trainers
def insert_trainers(connection):
    with connection.cursor() as cursor:
        trainers_data = [
            ('trainer1', 'password1', 'trainer1@example.com', 'Trainer 1'),
            ('trainer2', 'password2', 'trainer2@example.com', 'Trainer 2'),
            ('trainer3', 'password3', 'trainer3@example.com', 'Trainer 3'),
            ('trainer4', 'password4', 'trainer4@example.com', 'Trainer 4'),
            ('trainer5', 'password5', 'trainer5@example.com', 'Trainer 5')
        ]

        for trainer_data in trainers_data:
            cursor.execute("""
                INSERT INTO Trainers (username, password, email, full_name)
                VALUES (%s, %s, %s, %s)
            """, trainer_data)

        # Commit the transaction
        connection.commit()

        print("Trainers inserted successfully!")

# Function to insert anonymous members
def insert_anonymous_members(connection, num_members):
    with connection.cursor() as cursor:
        try:
            for i in range(1, num_members + 1):
                username = f"anonymous{i}"
                password = f"password{i}"
                email = f"anonymous{i}@example.com"
                full_name = f"Anonymous {i}"
                birthdate = f"2000-01-01"  # Assume all anonymous members have the same birthdate for simplicity
                weight = random.uniform(45, 120)  # Random weight between 45 to 120 kg
                height = random.uniform(150, 200)  # Random height between 150 to 200 cm
                fitness_goal = f"Fitness goal for anonymous member {i}"

                cursor.execute("""
                    INSERT INTO Members (username, password, email, full_name, birthdate, weight, height, fitness_goal)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (username, password, email, full_name, birthdate, weight, height, fitness_goal))

            # Commit the transaction
            connection.commit()

            print(f"{num_members} anonymous members inserted successfully!")
        except psycopg2.Error as e:
            print("Error:", e)

# Function to register a new member
def register_member(connection, username, password, email, full_name, birthdate, weight, height, fitness_goal):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("INSERT INTO Members (username, password, email, full_name, birthdate, weight, height, fitness_goal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"),
                (username, password, email, full_name, birthdate, weight, height, fitness_goal)
            )
            connection.commit()
            print("Registration successful!")
        except Exception as e:
            print("Error:", e)

# Function to delete a membership
def delete_membership(connection, member_id):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("DELETE FROM Members WHERE member_id = %s"),
                (member_id,)
            )
            connection.commit()
            print("Membership deleted successfully!")
        except psycopg2.Error as e:
            print("Error:", e)

# Function to register a new Admin staff
def register_admin(connection, username, password, email, full_name):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("INSERT INTO AdministrativeStaff (username, password, email, full_name) VALUES (%s, %s, %s, %s)"),
                (username, password, email, full_name)
            )
            connection.commit()
            print("Registration successful!")
        except Exception as e:
            print("Error:", e)

# Function to insert fitness goals for a member
def insert_fitness_goal(connection, member_id, goal_description, goal_date):
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    sql.SQL("INSERT INTO FitnessGoals (member_id, goal_description, goal_date) VALUES (%s, %s, %s)"),
                    (member_id, goal_description, goal_date)
                )
                connection.commit()
                print("Fitness goal inserted successfully!")
            except Exception as e:
                print("Error:", e)

# Function to update member profile
def update_member_profile(connection, member_id, full_name, birthdate, weight, height, fitness_goal):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("UPDATE Members SET full_name = %s, birthdate = %s, weight = %s, height = %s, fitness_goal = %s WHERE member_id = %s"),
                (full_name, birthdate, weight, height, fitness_goal, member_id)
            )
            connection.commit()
            print("Profile updated successfully!")
        except Exception as e:
            print("Error:", e)

# Function to update class schedule
def update_class_schedule(connection, class_id, class_name, trainer_id, max_capacity, class_time, duration):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("UPDATE Classes SET class_name = %s, trainer_id = %s, max_capacity = %s, class_time = %s, duration = %s WHERE class_id = %s"),
                (class_name, trainer_id, max_capacity, class_time, duration, class_id)
            )
            connection.commit()
            print("Class schedule updated successfully!")
        except Exception as e:
            print("Error:", e)

# Function to update equipment information
def update_equipment(connection, equipment_id, equipment_name, purchase_date, maintenance_interval, last_maintenance_date):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("UPDATE Equipment SET equipment_name = %s, purchase_date = %s, maintenance_interval = %s, last_maintenance_date = %s WHERE equipment_id = %s"),
                (equipment_name, purchase_date, maintenance_interval, last_maintenance_date, equipment_id)
            )
            connection.commit()
            print("Equipment information updated successfully!")
        except Exception as e:
            print("Error:", e)

# Function to delete equipment
def delete_equipment(connection, equipment_id):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("DELETE FROM Equipment WHERE equipment_id = %s"),
                (equipment_id,)
            )
            connection.commit()
            print("Equipment deleted successfully!")
        except Exception as e:
            print("Error:", e)

# Function to insert equipment item for maintenance modeling
def insert_equipment(connection, equipment_name, purchase_date, maintenance_interval, last_maintenance_date):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Equipment (equipment_name, purchase_date, maintenance_interval, last_maintenance_date)
                VALUES (%s, %s, %s, %s)
            """, (equipment_name, purchase_date, maintenance_interval, last_maintenance_date))
            
            # Commit the transaction
            connection.commit()

            print("Equipment inserted successfully!")
    except psycopg2.Error as e:
        print("Error:", e)
# Function to book a class
def book_class(connection, member_id, class_id, booking_time):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ClassBookings (member_id, class_id, booking_time)
                    VALUES (%s, %s, %s);
                """, (member_id, class_id, booking_time))

            # Commit the transaction after executing the SQL query
            connection.commit()

            print("Class booked successfully!")
        except psycopg2.Error as e:
            print("Error:", e)

# Function to cancel a class booking
def cancel_class_booking(connection, booking_id):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("DELETE FROM ClassBookings WHERE booking_id = %s"),
                (booking_id,)
            )
            connection.commit()
            print("Class booking canceled successfully!")
        except psycopg2.Error as e:
            print("Error:", e)

#Function to view all members
def view_all_members(connection):
    with connection.cursor() as cursor:
        try: 
            cursor.execute("SELECT * FROM Members")
            records = cursor.fetchall()

            # Print the records
            for record in records:
                print(record)
            connection.commit()
            print("Displaying all members currently registered in our system!")
        except Exception as e:
            print("Error:", e)


# Function to schedule personal training session
def schedule_training_session(connection, member_id, trainer_id, session_time, duration):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("INSERT INTO PersonalTrainingSessions (member_id, trainer_id, session_time, duration) VALUES (%s, %s, %s, %s)"),
                (member_id, trainer_id, session_time, duration)
            )
            connection.commit()
            print("Training session scheduled successfully!")
        except Exception as e:
            print("Error:", e)

# Function to process payment
def process_payment(connection, member_id, amount):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                sql.SQL("INSERT INTO Payments (member_id, amount) VALUES (%s, %s)"),
                (member_id, amount)
            )
            connection.commit()
            print("Payment processed successfully!")
        except Exception as e:
            print("Error:", e)

def main():
    connection = connect()
    create_tables(connection)
    insert_trainers(connection)
    insert_anonymous_members(connection, 10)
    insert_initial_data(connection)

    while True:
        print("\nAre you a Member, Trainer or Administrative Staff")
        choice1 = input("\nEnter your choice: ")

        if choice1 == 'Member':   
            print("\nAvailable commands:")
            print("registerMember -> register a new member")
            print("deleteMembership -> delete a member")
            print("updateMemberProfile -> update member profile")
            print("setFitnessGoal -> set member fitness goal")
            print("scheduleTrainingSession -> schedule personal training session")

            choice = input("\nEnter your choice: ")

            if choice == 'registerMember':
                username = input("Enter user name: ")
                password = input("Enter password: ")
                email = input("Enter email: ")
                full_name = input("Enter full-name: ")
                birthdate = input("Enter birthdate (YYYY-MM-DD): ")
                weight = input("Enter weight: ")
                height = input("Enter height: ")
                fitness_goal = input("Enter fitness goal: ")
                register_member(connection, username, password, email, full_name, birthdate, weight, height, fitness_goal)
            elif choice == 'deleteMembership':
                member_id = input("Enter member id: ")
                delete_membership(connection, member_id)
            elif choice == "setFitnessGoal":
                member_id = input("Enter member id: ")
                goal_description = input("Enter goal description: ")
                goal_date = input("Enter enter anticipated goal date: ")
                insert_fitness_goal(connection, member_id, goal_description, goal_date)
            elif choice == 'updateMemberProfile':
                member_id = input("Enter member id: ")
                full_name = input("Enter full-name: ")
                birthdate = input("Enter birthdate (YYYY-MM-DD): ")
                weight = input("Enter weight: ")
                height = input("Enter height: ")
                fitness_goal = input("Enter fitness goal: ")
                update_member_profile(connection, member_id, full_name, birthdate, weight, height, fitness_goal)
            elif choice == 'scheduleTrainingSession':
                member_id = input("Enter member id: ")
                trainer_id = input("Enter trainer id: ")
                session_time = input("Enter session time: ")
                duration = input("Enter duration: ")
                schedule_training_session(connection, member_id, trainer_id, session_time, duration)
            elif choice == 'exit':
                break
            else:
                print("Invalid choice. Please try again.")
        elif choice1 == 'Trainer':
            print("\nAvailable commands:")
            print("viewAllMembers -> show all members registered")

            choice = input("\nEnter your choice: ")

            if choice == "viewAllMembers":
                view_all_members(connection)
            elif choice == 'exit':
                break
            else:
                print("Invalid choice. Please try again.")
        elif choice1 == 'Administrative Staff':
            print("\nAvailable commands:")
            print("registerAdminStaff -> register a new Administrative staff")
            print("bookClass -> book a class")
            print("cancelClassBooking -> cancel a class")
            print("updateClassSchedule -> update the class schedule")
            print("insertEquipment -> Inserting a new piece of equipment for maintenance")
            print("updateEquipment -> update the equipments data")
            print("deleteEquipment -> delete equipment data")
            print("processPayment -> process payment")
            print("exit -> Exit")

            choice = input("\nEnter your choice: ")

            if choice == 'registerAdminStaff':
                username = input("Enter user name: ")
                password = input("Enter password: ")
                email = input("Enter email: ")
                full_name = input("Enter full-name: ")
                register_admin(connection, username, password, email, full_name)
            elif choice == 'bookClass':
                member_id = input("Enter member id: ")
                print("Here are the class Id related classes:\t1 = Yoga\t2 = Pilates\t3 = Spinning\t4 = Zumba\t5 = Bootcamp")
                class_id = input("Enter class id: ")
                booking_time = input("Enter booking time: ")
                book_class(connection, member_id, class_id, booking_time)
            elif choice == 'cancelClassBooking':
                booking_id = input("Enter booking id: ")
                cancel_class_booking(connection, booking_id)
            elif choice == "updateClassSchedule":
                class_id = input("Enter class id: ")
                class_name = input("Enter class name: ")
                trainer_id = input("Enter trainer id: ")
                max_capacity = input("Enter max capacity: ")
                class_time = input("Enter class time: ")
                duration = input("Enter class duration: ")
                update_class_schedule(connection, class_id, class_name, trainer_id, max_capacity, class_time, duration)
            elif choice == 'insertEquipment':
                equipment_name = input("Enter Equipment name: ")
                purchase_date = input("Enter Purchase Date: ")
                maintenance_interval = input("Enter Maintenance interval: ")
                last_maintenance_date = input("Enter last maintenance date: ")
                insert_equipment(connection, equipment_name, purchase_date, maintenance_interval, last_maintenance_date)
            elif choice == "updateEquipment":
                equipment_id = input("Enter equipment Id: ")
                equipment_name = input("Enter Equipment name: ")
                purchase_date = input("Enter Purchase Date: ")
                maintenance_interval = input("Enter Maintenance interval: ")
                last_maintenance_date = input("Enter last maintenance date: ")
                update_equipment(connection, equipment_id, equipment_name, purchase_date, maintenance_interval, last_maintenance_date)
            elif choice == "deleteEquipment":
                equipment_id = input("Enter equipment Id: ")
                delete_equipment(connection, equipment_id)
            elif choice == 'processPayment':
                member_id = input("Enter member id: ")
                amount = input("Enter amount: ")
                process_payment(connection, member_id, amount)
            elif choice == 'exit':
                break
            else:
                print("Invalid choice. Please try again.")

    connection.close()

if __name__ == "__main__":
    main()
