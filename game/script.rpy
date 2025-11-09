# ==================================================================
# КЛИКАБЕЛЬНЫЙ ФОН КОМНАТЫ ГГ И КОСТИКА
# ==================================================================
init:
    define dormroom_food = False
    define dormroom_bag = False
    define dormroom_mystuff = False
    define dormroom_kostikshit = False
    define dormroom_shower = False
    define dormroom_kostik = True
    define dormroom_dressup = False
    define dormroom_exit = False
    define ask_1 = False

    define dormroom_food_seen = 0
    define dormroom_bag_seen = 0
    define dormroom_mystuff_seen = 0
    define dormroom_kostikshit_seen = 0
    define dormroom_shower_seen = 0
    define dormroom_kostik_seen = 0
    define dormroom_dressup_seen = 0
    define dormroom_exit_seen = 0

    define dormroom_skillet = False

    image dormroom = "dormroom.jpg"
    image me = "me.png"
    image ko = "ko.png"

screen dormroom_screen:

    modal True
    add "dormroom.jpg"

    if not dormroom_food:
        imagebutton:
            auto "dormroom_food_%s.png"
            focus_mask True
            xpos 902
            ypos 71
            action Return("dormroom_food")

    if not dormroom_bag:
        imagebutton:
            auto "dormroom_bag_%s.png"
            focus_mask True
            xpos 948
            ypos 751
            action Return("dormroom_bag")

    if not dormroom_mystuff:
        imagebutton:
            auto "dormroom_mystuff_%s.png"
            focus_mask True
            xpos 680
            ypos 305
            action Return("dormroom_mystuff")

    if not dormroom_kostikshit:
        imagebutton:
            auto "dormroom_kostikshit_%s.png"
            focus_mask True
            xpos 482
            ypos 500
            action Return("dormroom_kostikshit")

    if not dormroom_shower:
        imagebutton:
            auto "dormroom_shower_%s.png"
            focus_mask True
            xpos 942
            ypos 191
            action Return("dormroom_shower")

    if not dormroom_kostik:
        imagebutton:
            auto "dormroom_kostik_%s.png"
            focus_mask True
            xpos 782
            ypos 182
            action Return("dormroom_kostik")

    if not dormroom_dressup:
        imagebutton:
            auto "dormroom_dressup_%s.png"
            focus_mask True
            xpos 1467
            ypos 479
            action Return("dormroom_dressup")

    if not dormroom_exit:
        imagebutton:
            auto "dormroom_exit_%s.png"
            focus_mask True
            xpos 0
            ypos 0
            action Return("dormroom_exit")
















# ==================================================================
# ИНВЕНТАРЬ И ПРЕДМЕТЫ (https://discover-with-mia.itch.io/free-source-code-renpy-python-multipage-inventory-system)
# ==================================================================

init python:
    class Item:
        def __init__(self, name, stack, weight, description):
            self.name = name
            self.stack = stack
            self.weight = weight
            self.description = description

    def create_items():
        items = {}
        items["Сковородка"] = Item(
            name="Сковородка",
            stack=1,
            weight=2,
            description="Дешевая сковородка из магазина под домом."
        )
        return items

default items = create_items()

init python:
    class Inventory:
        def __init__(self, slot_count=15, unlocked_slots=0):
            self.slot_count = slot_count
            self.unlocked_slots = unlocked_slots
            self.slots = [{} for _ in range(self.slot_count)]

        def add_item(self, item, quantity):
            renpy.notify(f"{item} +{quantity}")
            if self.unlocked_slots == 0:
                return
            remaining_quantity = quantity
            for slot in range(self.unlocked_slots):
                if item in self.slots[slot]:
                    space_left = item.stack - self.slots[slot][item]
                    if space_left > 0:
                        add_quantity = min(remaining_quantity, space_left)
                        self.slots[slot][item] += add_quantity
                        remaining_quantity -= add_quantity
                        if remaining_quantity == 0:
                            return
            for slot in range(self.unlocked_slots):
                if not self.slots[slot]:
                    add_quantity = min(remaining_quantity, quantity)
                    self.slots[slot][item] = add_quantity
                    remaining_quantity -= add_quantity
                    if remaining_quantity == 0:
                        return

        def remove_item(self, item, quantity=1):
            if quantity <= 0:
                return
            original_quantity = quantity
            for slot in range(self.slot_count):
                if item in self.slots[slot]:
                    if quantity >= self.slots[slot][item]:
                        quantity -= self.slots[slot][item]
                        del self.slots[slot][item]
                    else:
                        self.slots[slot][item] -= quantity
                        quantity = 0
                    if quantity <= 0:
                        break
            if quantity > 0:
                self.sort_inventory()
            else:
                self.sort_inventory()

        def sort_inventory(self):
            sorted_slots = [{} for _ in range(self.slot_count)]
            current_slot = 0

            for slot in range(self.slot_count):
                if self.slots[slot]:
                    sorted_slots[current_slot] = self.slots[slot]
                    current_slot += 1
            self.slots = sorted_slots

        def increase_slot_count(self, additional_slots):
            self.slot_count += additional_slots
            self.slots.extend([{} for _ in range(additional_slots)])

        def unlock_slots(self, count):
            self.unlocked_slots = min(self.slot_count, self.unlocked_slots + count)
            renpy.notify(f"Инвентарь +{self.unlocked_slots}")

        def is_slot_unlocked(self, slot):
            return slot < self.unlocked_slots

        def lock_slots(self, count):
            if count <= self.unlocked_slots:
                self.unlocked_slots -= count

        def get_items(self):
            return self.slots

        def has_item(self, item, quantity=1):
            total = 0
            for slot in self.slots:
                if item in slot:
                    total += slot[item]
            return total >= quantity

screen inventory():
    tag ALBE
    modal True
    default current_description = ""
    frame:
        xalign 0.5
        yalign 0.5
        padding (20, 20)
        vbox:
            label "Инвентарь" xalign 0.5
            text "[current_description]" size 20 xalign 0.5
            spacing 20
            hbox:
                spacing 20
                grid 5 3:
                    xalign 0.5
                    yalign 0.5
                    spacing 20
                    transpose False
                    for slot in range(inventory.slot_count):
                        if inventory.is_slot_unlocked(slot):
                            frame:
                                xsize 150
                                ysize 150
                                if inventory.slots[slot]:
                                    for item_name, quantity in inventory.slots[slot].items():
                                        $ current_item = items[item_name]
                                        add Image(item_name + ".png") xalign 0.5 yalign 0.5 size (100, 100)
                                        $ Inv_item_quantity = f"x{quantity}"
                                        text "[item_name]":
                                            size 15
                                            pos (2,0)
                                        text Inv_item_quantity:
                                            size 12
                                            text_align 1.0
                                            pos (135, 135)
                                            xanchor 1.0
                                            yanchor 1.0
                                        button:
                                             hovered SetScreenVariable ("current_description", current_item.description)
                                             unhovered SetScreenVariable ("current_description", "")
                                             action NullAction()
                                             xfill True
                                             yfill True
                                else:
                                    null
                        else:
                            null
            textbutton "Закрыть" xalign 0.5:
                action Hide("inventory")










# ==================================================================
# ХАРАКТЕРИСТИКИ ПЕРСОНАЖА (https://youtu.be/vLfZelNH_ho?si=8atyXN9oNsHOC3Bl)
# ==================================================================

init python:
    class Actor:
        def __init__(self, character, name, stats, status):
            self.c = character
            self.name = name
            self.stats = {
                "Атлетика": 0,
                "Мышление": 0,
                "Общение": 0,
                "Баланс": 0
            }

            for key, value in stats.items():
                if key in self.stats:
                    self.stats[key] = value

        @property
        def health(self):
            return self.stats['Атлетика'] * 5
        @property
        def max_health(self):
            return self.health
        @property
        def weight(self):
            return self.stats['Атлетика'] * 2
        @property
        def rating(self):
            return self.stats['Общение'] * 5
        @property
        def status(self):
            return {
                "Здоровье": self.health,
                "Макс. здоровье": self.max_health,
                "Носимый вес": self.weight,
                "Рейтинг": self.rating
            }

        def change_stat(self, stat_name, amount):
            self.stats[stat_name] += amount
            if amount > 0:
                renpy.notify(f"{stat_name} +{amount}")
            else:
                renpy.notify(f"{stat_name} -{amount}")

        def change_status(self, status_name, amount):
            self.status[status_name] += amount
            if amount > 0:
                renpy.notify(f"{status_name} +{amount}")
            else:
                renpy.notify(f"{status_name} -{amount}")

define me = Actor(Character("Ты", color="#c8ffc8"), "Ты", {"Атлетика": 15, "Мышление": 9, "Общение": 12, "Баланс": 500}, {})
define ko = Actor(Character("Костик", color="#1a4780"), "Костик", {"Атлетика": 20, "Мышление": 8, "Общение": 8, "Баланс": 1000}, {})

screen statistics():
    tag ALBE
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        hbox:
            spacing 40
            vbox:
                spacing 10
                text "Здоровье" size 40
                text "Баланс" size 40
                text "Носимый вес" size 40
                text "Рейтинг" size 40
                text "Атлетика" size 40
                text "Мышление" size 40
                text "Общение" size 40
                textbutton _("Закрыть") action Hide("statistics")
            vbox:
                spacing 10
                text "[me.status['Здоровье']]"+"/"+"[me.status['Макс. здоровье']]"+" HP" size 40
                text "[me.stats['Баланс']]"+" мон." size 40
                text "[me.status['Носимый вес']]"+" кг"size 40
                text "[me.status['Рейтинг']]" size 40
                text "[me.stats['Атлетика']]" size 40
                text "[me.stats['Мышление']]" size 40
                text "[me.stats['Общение']]" size 40









# ==================================================================
# КВЕСТОВАЯ СИСТЕМА
# ==================================================================

init python:
    class Quest:

        UNKNOWN = "неизвестен"
        ACTIVE = "получен"
        COMPLETED = "завершен"

        def __init__(self, title, description, state=UNKNOWN):
            self.title = title
            self.description = description
            self.state = state

        def change_quest_status(self, new_state):
            self.state = new_state
            renpy.notify(f"Квест {self.title} – {self.state}")

    if "quests" not in globals():
        quests = []

screen quests():
    tag ALBE
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        vbox:
            spacing 70
            vbox:
                spacing 10
                text "{b}Активные квесты{/b}"
                for quest in quests:
                    if quest.state == Quest.ACTIVE:
                        text "[quest.title]:"
                        text "{alpha=0.6}[quest.description]{/alpha}"
            vbox:
                spacing 10
                text "{b}Закрытые квесты{/b}"
                for quest in quests:
                    if quest.state == Quest.COMPLETED:
                        text "{alpha=0.6}[quest.title]{/alpha}"
            textbutton _("Закрыть") action Hide("quests")

default quest_dormroom_grass = Quest(title = "Потрогать траву", description = "Мне надо выйти из дома и поехать в институт.")
default quest_dormroom_shower = Quest(title = "Принять душ", description = "После весёлой ночи мне стоит освежиться.")
default quest_dormroom_clothes = Quest(title = "Одеться", description = "На улице не принято ходить голым.")
default quest_dormroom_breakfast = Quest(title = "Позавтракать", description = "Голод не тётка. А как там дальше?")
default quest_dormroom_stuff = Quest(title = "Собрать вещи", description = "Не стоит идти в институт с пустыми руками")

label start:
    $ quests.append(quest_dormroom_grass)
    $ quests.append(quest_dormroom_shower)
    $ quests.append(quest_dormroom_clothes)
    $ quests.append(quest_dormroom_breakfast)
    $ quests.append(quest_dormroom_stuff)
    jump dormroom_quests









# ==================================================================
# ДОСТИЖЕНИЯ
# ==================================================================












# ==================================================================
# СЦЕНАРИЙ
# ==================================================================

# Инициализация инвентаря
default inventory = Inventory()

label dormroom_quests:
    $ save_name = ('Протокол отчисления. Технодемка')
    $ renpy.block_rollback()
    $ renpy.pause(1, hard = True)
    scene dormroom with dissolve
    pause(1.5)
    $ quest_dormroom_grass.change_quest_status(Quest.ACTIVE)
    pause(1.5)
    $ quest_dormroom_shower.change_quest_status(Quest.ACTIVE)
    pause(1.5)
    $ quest_dormroom_clothes.change_quest_status(Quest.ACTIVE)
    pause(1.5)
    $ quest_dormroom_breakfast.change_quest_status(Quest.ACTIVE)
    pause(1.5)
    $ quest_dormroom_stuff.change_quest_status(Quest.ACTIVE)
    pause(1.5)
    jump dormroom


label dormroom:
    call screen dormroom_screen()
    $ result = _return

    if result == "dormroom_bag":
        $ dormroom_bag_seen += 1
        $ dormroom_bag = True
        "Ты поднимаешь с пола свою сумку."
        "Теперь у тебя появилась возможность носить с собой вещи!"
        show me at left with dissolve
        me.c "Круто!"
        $ inventory.unlock_slots(10)
        jump dormroom

    if result == "dormroom_mystuff":
        if dormroom_mystuff_seen == 0:
            $ dormroom_mystuff_seen += 1
            "Ты подходишь к хаотично раскиданному хламу – твоим вещам."
        if not dormroom_bag:
            show me at left with dissolve
            me.c "Сначала надо найти, куда всё это сложить."
            jump dormroom
        else:
            $ dormroom_mystuff += 1
            $ inventory.add_item("Сковородка", 1)
            "Ты складываешь всё необходимое в свою сумку."
            $ quest_dormroom_stuff.change_quest_status(Quest.COMPLETED)
            show me at left with dissolve
            me.c "Так. А теперь что?"
            jump dormroom

    if result == "dormroom_kostikshit":
        if dormroom_kostikshit_seen == 0:
            $ dormroom_kostikshit_seen += 1
            "Это тумбочка с вещами твоего соседа."
            "Она как обычно заперта на замок."
            show me at left with dissolve
            me.c "Вероятно, он откроет её, когда выйдет из душа."
            jump dormroom
        else:
            "Тумбочка заперта."
            jump dormroom
        menu:
            "Подобрать":
                if not dormroom_bag:
                    me.c "И куда я это положу? Нужна сумка."
                    jump dormroom
                else:
                    $ dormroom_kostikshit = True
                    $ dormroom_skillet = True
                    $ inventory.add_item("Сковородка", 1)
                    "Ты подобрал сковородку."
                    jump dormroom
            "Не подбирать":
                $ dormroom_kostikshit = True
                me.c "Ну на фиг."
                jump dormroom

    if result == "dormroom_shower":
        if not dormroom_mystuff:
            if dormroom_shower_seen == 0:
                $ dormroom_shower_seen += 1
                "Ты заглядываешь в душ и видишь, как там полощется твой сосед."
                show me at left with dissolve
                me.c "Ладно."
                me.c "Пока что можно собрать вещи."
                jump dormroom
            else:
                "Душ всё ещё занят."
                jump dormroom
        else:
            $ dormroom_shower = True
            "Твой сосед как раз закончил умываться и впустил тебя внутрь."
            show me at left with dissolve
            me.c "Теперь надо как следует отдраиться!"
            "После пяти минут жесткой помывки ты чувствуешь себя посвежевшим и готовым к новым свершениям!"
            $ quest_dormroom_shower.change_quest_status(Quest.COMPLETED)
            $ dormroom_kostik = False
            jump dormroom

    if result == "dormroom_kostik":
        show me at left with dissolve
        show ko at right with dissolve
        if dormroom_kostik_seen == 0:
            $ dormroom_kostik_seen += 1
            "Ты смотришь на своего соседа."
            "Он немного старше тебя, но несмотря на это вы нормально общаетесь."
            "Костик перехватил твой взгляд и улыбнулся."
            ko.c "Опять пойдёшь кутить?"
            me.c "Нет, в этот раз нужно в уник ехать."
            ko.c "Это хорошо. Мужик должен быть умным!"
            ko.c "Тебе что-то нужно?"
        else:
            ko.c "Чего тебе?"
        menu:
            "А где сковородка?" if dormroom_food_seen > 0 and not dormroom_skillet:
                ko.c "Понятия не имею!"
                jump dormroom
            "Зачем ты украл сковородку?" if dormroom_skillet and not ask_1:
                $ ask_1 = True
                ko.c "Я просто забыл положить её обратно."
                with hpunch
                ko.c "Ты рылся в моих вещах!?"
                me.c "Я взял только сковородку!"
                jump dormroom
            "Давай армрестлинг!":
                ko.c "Давай!"
                pause(2)
                with hpunch
                "Ты проиграл!"
                if me.stats['Атлетика'] > 15:
                    "Но Костику пришлось попотеть!"
                    ko.c "Хорошо получилось! Ещё немного и дойдёшь до моего уровня!"
                else:
                    ko.c "Не печалься! Может, в следующий раз получится!"
                jump dormroom

    if result == "dormroom_food":
        if not dormroom_shower:
            show me at left with dissolve
            me.c "Кушать, конечно, хочется, но сначала лучше принять душ."
            jump dormroom
        if not dormroom_skillet:
            $ dormroom_food_seen += 1
            "Ты подходишь к вашей микрокухне с намерением приготовить яичницу."
            show me at left with dissolve
            me.c "А где сковородка?{w=0.5} Чёрт…"
            me.c "Я же только-только новую купил!"
            "Кажется, тебе придется довольствоваться чем-то другим."
            jump dormroom
        else:
            $ dormroom_food = True
            if dormroom_skillet:
                show me at left with dissolve
                "Ты ставишь сковородку на конфорку, добавляешь масла."
                "Разбиваешь пару яиц и делаешь…"
                menu:
                    "Глазунью разума":
                        pause(2)
                        $ me.change_stat("Мышление", 2)
                    "Омлет общения":
                        pause(2)
                        $ me.change_stat("Общение", 2)
                    "Скрамбл силы":
                        pause(2)
                        $ me.change_stat("Атлетика", 2)
                "Спустя пару минут у тебя в тарелке уже был полезный перекус."
                with fade
                "Ты с удовольствием позавтракал!"
                "{b}Достижение получено: Яичница!{/b}"
                $ quest_dormroom_breakfast.change_quest_status(Quest.COMPLETED)
                jump dormroom
            else:
                show me at left with dissolve
                me.c "С яичницей не сложилось, что тут ещё есть?"
                menu:
                    "Бутерброды с чаем":
                        "Обычный завтрак студента. Простенько и со вкусом."
                    "Хлопья с молоком":
                        "Сладкие хлопья с молоком навевают воспоминания о детстве."
                    "Чипсы с пивом":
                        "Вредная пища никогда не повредит. Или нет?"
                $ quest_dormroom_breakfast.change_quest_status(Quest.COMPLETED)
                jump dormroom

    if result == "dormroom_dressup":
        if dormroom_dressup_seen == 0:
            $ dormroom_dressup_seen += 1
            "Шкаф с твоими модными нарядами."
            "Сейчас твой гардероб сравнительно небольшой, но со временем ты сможешь его расширить!"
        if dormroom_shower == 0:
            me.c "Сначала, наверное, стоит принять душ, чтобы два раза не переодеваться."
            jump dormroom
        else:
            $ dormroom_dressup = True
            me.c "Самое время выбрать себе наряд получше!"
            $ quest_dormroom_clothes.change_quest_status(Quest.COMPLETED)
            "Закончив с переодеванием, ты ещё раз осмотрел свою комнату."
            jump dormroom

    if result == "dormroom_exit":
        show me at left with dissolve
        if not dormroom_shower:
            me.c "Преподы учуют запах раздолбая за километр."
            me.c "Пожалуй, перед выходом мне стоит принять душ."
            jump dormroom
        elif not dormroom_mystuff:
            me.c "А как же мои вещи? Надо собраться!"
            jump dormroom
        elif not dormroom_dressup:
            me.c "В таком виде я никуда не пойду."
            me.c "Для начала нужно одеться."
            jump dormroom
        else:
            if not dormroom_food:
                "Твой живот урчит, требуя подзарядки."
            "После непродолжительных сборов ты толкаешь дверь и выходишь на улицу."
            jump dormroom
