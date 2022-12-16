import random

from datacenter.models import (Schoolkid, Mark, Chastisement,
                                Lesson, Subject, Commendation, Teacher)


COMMENDATIONS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!",
]


def fix_marks(schoolkid, bad_marks=[2, 3], good_mark=5):
    Mark.objects.filter(schoolkid=schoolkid).filter(points__in=bad_marks).update(points=good_mark)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def choose_subject_title(schoolkid):
    return random.choice(Subject.objects.filter(year_of_study=schoolkid.year_of_study)).title


def create_commendation(schoolkid, subject_title=None):
    text = random.choice(COMMENDATIONS)
    if not subject_title:
        subject_title = choose_subject_title(schoolkid)
    subjects = Subject.objects.filter(
                    title__contains=subject_title,
                    year_of_study=schoolkid.year_of_study,
                )
    if not subjects:
        print("Предмет не найден! Уточните название предмета.")
    elif len(subjects) > 1:
        print("Найдено более одного совпадения! Уточните название предмета.")
    else:
        subject = subjects.first()
        lessons = Lesson.objects.filter(
                        subject=subject,
                        group_letter=schoolkid.group_letter,
                    ).order_by("-date")
        last_lesson = lessons.first()
        Commendation.objects.create(
            text=text,
            created=last_lesson.date,
            schoolkid=schoolkid,
            subject=subject,
            teacher=last_lesson.teacher,
        )


def get_schoolkid(name="Фролов Иван Григорьевич"):
    if not name:
        return print("Отсутствует ФИО!")
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print("\n\n\n\n\nСовпадений не найдено! Уточните ФИО ученика.\n\n\n\n\n")
        raise
    except Schoolkid.MultipleObjectsReturned:
        print("\n\n\n\n\nНайдено более одного совпадения! Уточните ФИО ученика.\n\n\n\n\n")
        raise


def main():
    schoolkid = get_schoolkid()
    if schoolkid:
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid)


if __name__ == "__main__":
    main()
