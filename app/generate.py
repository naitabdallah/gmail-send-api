import csv
import random

# List of names
names = [
    "Emily,Johnson", "Michael,Smith", "Jennifer,Brown", "Christopher,Davis", "Sarah,Wilson",
    "Matthew,Jones", "Amanda,Taylor", "David,Martinez", "Jessica,Anderson", "James,Thomas",
    "Ashley,Garcia", "John,Rodriguez", "Brittany,Lopez", "Robert,Lee", "Samantha,Perez",
    "Daniel,Harris", "Elizabeth,Gonzalez", "Joseph,Clark", "Megan,Lewis", "William,Walker",
    "Lauren,King", "Nicholas,White", "Kayla,Hall", "Andrew,Scott", "Stephanie,Turner",
    "Ryan,Young", "Taylor,Allen", "Brandon,Martinez", "Heather,Wright", "Joshua,Miller",
    "Rebecca,Moore", "Justin,Hernandez", "Amber,Jackson", "Benjamin,Adams", "Danielle,Hill",
    "Kevin,Baker", "Courtney,Green", "Timothy,Nelson", "Rachel,Ramirez", "Nathan,Carter",
    "Michelle,Campbell", "Zachary,Mitchell", "Emily,Reed", "Alexander,Torres", "Samantha,Roberts",
    "Jacob,Murphy", "Victoria,Rivera", "Cody,Ward", "Lauren,Bailey", "Kyle,Phillips",
    "Erin,Howard", "Brian,Coleman", "Kaitlyn,Diaz", "Anthony,Washington", "Laura,Morris",
    "Caleb,Sanchez", "Olivia,Price", "Sean,Barnes", "Alyssa,Perry", "Eric,Watson", "Christina,Butler",
    "Gregory,Foster", "Tara,Gray", "Patrick,Powell", "Anna,Russell", "Stephen,Long", "Julia,Diaz",
    "Jeffrey,Stewart", "Maria,Reyes", "Dylan,Nguyen", "Alexis,Martinez", "Keith,Evans", "Lindsey,Bell",
    "Randy,Cox", "Holly,Hughes", "Peter,Fisher", "Shannon,Coleman", "Douglas,Richardson",
    "Monica,Simmons", "Travis,Ross", "Courtney,Perry", "Kenneth,Patterson", "Kristin,Brooks",
    "Gabriel,Kelly", "Diana,Bailey", "Steven,Henderson", "Carly,Coleman", "Martin,James",
    "Erin,Brooks", "Christian,Howard", "Sandra,Ward", "Jordan,Ross", "Angela,Nelson",
    "Juan,Murphy", "Kimberly,Coleman", "Logan,Price", "Valerie,Cox", "Phillip,Russell",
    "Lisa,Ortiz", "Samuel,Ramirez"
]

# Function to generate random emails
def generate_email(first_name, last_name):
    domain = "@beastofthe.online"
    first_name = first_name.lower()
    last_name = last_name.lower()
    rand_num = random.randint(100, 999)
    email = f"{first_name}.{last_name}{rand_num}{domain}"
    return email

# Number of users to generate
num_users = 100

# Open CSV file for writing
with open('user_list.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['email', 'password', 'givenName', 'familyName'])

    # Generate users
    for _ in range(num_users):
        name = random.choice(names).split(',')
        first_name = name[0]
        last_name = name[1]
        password = "Password123@"
        email = generate_email(first_name, last_name)
        writer.writerow([email, password, first_name, last_name])

print("CSV file generated successfully.")


with open ('user_list.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)