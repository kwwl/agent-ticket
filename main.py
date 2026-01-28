from mail_management import send_mail
from ticket_agent import generate_ticket_mail
import pandas
import time


def create_tickets_problems(number_of_problems=150):
    number_of_batches = number_of_problems // 5

    list_of_ids = []
    list_of_subjects = []
    list_of_categories = []
    index_batch = 0

    while index_batch < number_of_batches:
        try:
            print(f"Batch number {index_batch}:")

            ticket_response = generate_ticket_mail()

            for index_mail, mail in ticket_response.items():

                subject = mail["sujet"]
                message = mail["contenu"]
                category = mail["categorie"]

                send_mail(subject, message)

                id_mail = f'b{index_batch}_m{index_mail.split("_")[1]}'
                print(id_mail)
                print(subject)
                print(message)
                print(category)
                print("_" * 20)

                list_of_ids.append(id_mail)
                list_of_subjects.append(subject)
                list_of_categories.append(category)

            print(f"End batch {index_batch}")
            index_batch += 1
            print("_" * 40)

        except:
            print("Le batch a échoué, nous allons retenter notre chance ;)")
            time.sleep(5)

    pandas.DataFrame(
        {
            "ids": list_of_ids,
            "subjects": list_of_subjects,
            "categories": list_of_categories,
        },
    ).to_csv("ground_truth.csv", index=False)


if __name__ == "__main__":
    create_tickets_problems(number_of_problems=500)
