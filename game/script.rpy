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
# ИНВЕНТАРЬ (https://github.com/Patchmonk/Enhanced-Renpy-Inventory/tree/master)
# ==================================================================

init python:
    class Inventory:
        def __init__(self, slot_count=15, unlocked_slots=0):
            self.slot_count = slot_count
            self.unlocked_slots = unlocked_slots
            self.max_items_per_slot = 1
            self.slots = [{} for _ in range(self.slot_count)]

        def add_item(self, item, quantity=1):
            renpy.notify(f"{item} +{quantity}")
            if self.unlocked_slots == 0:
                return

            remaining_quantity = quantity

            # First, try to add to existing slots with the same item
            for slot in range(self.unlocked_slots):
                if item in self.slots[slot]:
                    space_left = self.max_items_per_slot - self.slots[slot][item]
                    if space_left > 0:
                        add_quantity = min(remaining_quantity, space_left)
                        self.slots[slot][item] += add_quantity
                        remaining_quantity -= add_quantity
                        if remaining_quantity == 0:
                            return

            # Next, try to add to empty slots
            for slot in range(self.unlocked_slots):
                if not self.slots[slot]:
                    add_quantity = min(remaining_quantity, self.max_items_per_slot)
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
                self.sort_inventory()  # Call sort_inventory after removal
            else:
                self.sort_inventory()  # Call sort_inventory after removal

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
            return total >= quantity  # Returns True if inventory has at least 'quantity' of item

# close icon 
image close:
    "close.png"
    size(30,30)
    
image close_hover:
    "close_hover.png"
    size(30,30)

style inventory_frame is frame:
    xsize 840
    ysize 570
    xalign 0.5
    yalign 0.5
    background "Inventory_frame_BG.png"

style close_btn:
    xpos 795
    ypos 5

style inventory_title:
    size 30
    pos (0, -20)
    color Color((222, 222, 222, 255))

style dummy is text:
    size 6

style inventory_container is vbox:
    xpos 30
    ypos 30

style inventory_grid is vpgrid:
    spacing 5

style inventory_scrollbar is scrollbar:
    xsize 1105
    ysize 450

style inventory_item_name is text:
    size 14
    bold True
    color Color((251, 251, 251, 255))
    pos (2,0)

style inventory_item_quantity is text:
    size 12
    bold True
    color Color((251, 251, 251, 255))
    text_align 1.0
    pos (135, 135)
    xanchor 1.0
    yanchor 1.0

style hud_frame is frame:
    xpadding 10
    ypadding 10
    xalign 0.5
    yalign 0.0

screen inventory():
    tag ALBE
    modal True
    frame:

        style "inventory_frame"
        hbox:
            imagebutton:
                style "close_btn"
                idle "close"
                hover "close_hover"
                action Hide("inventory")

        vbox:
            style "inventory_container"
            text "МОЙ ХАБАР" style "inventory_title"

            viewport id "vp":
                ysize 570
                draggable True
                mousewheel True
                scrollbars "vertical"
                vscrollbar_xsize 8
                vscrollbar_ysize 470
                vscrollbar_ypos 0
                vscrollbar_xpos -37
                vscrollbar_base_bar "inv_vscrollbar_base_bar.png" 
                vscrollbar_thumb "inv_vscrollbar_thumb.png"
                vscrollbar_unscrollable "hide"

                vpgrid cols 5:
                    style "inventory_grid"

                    for slot in range(inventory.slot_count):
                        frame:
                            maximum(155, 155)
                            if inventory.is_slot_unlocked(slot):
                                background Image("slot_bg.png")
                                if inventory.slots[slot]:
                                    for item, quantity in inventory.slots[slot].items():
                                        add Image(item + ".png") xalign 0.5 yalign 0.5 size (120, 120)
                                        $ Inv_item_name = item.replace('_', ' ')
                                        $ Inv_item_quantity = f"x{quantity}"
                                      
                                        text Inv_item_name style "inventory_item_name"
                                        text Inv_item_quantity style "inventory_item_quantity"
                            else:
                                background Image("locked_slot_bg.png")








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
        def __init__(self, name, description, available = False, completed = False):
            self.name = name
            self.description = description
            self.available = available
            self.completed = completed

        @property
        def should_show(self):
            if self.available and not self.completed:
                return True
            return False








# ==================================================================
# СЦЕНАРИЙ
# ==================================================================

# Инициализация инвентаря
default inventory = Inventory()

label start:

    $ save_name = ('Протокол отчисления. Технодемка')
    $ renpy.block_rollback()
    $ renpy.pause(1, hard = True)

    scene dormroom with dissolve
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
        jump start

    if result == "dormroom_mystuff":
        if dormroom_mystuff_seen == 0:
            $ dormroom_mystuff_seen += 1
            "Ты подходишь к хаотично раскиданному хламу – твоим вещам."
        if not dormroom_bag:
            show me at left with dissolve
            me.c "Сначала надо найти, куда всё это сложить."
            jump start
        else:
            $ dormroom_mystuff += 1
            $ inventory.add_item("Картошка", quantity=5)
            "Ты складываешь всё необходимое в свою сумку."
            show me at left with dissolve
            me.c "Так. А теперь что?"
            jump start

    if result == "dormroom_kostikshit":
        if dormroom_kostikshit_seen == 0:
            $ dormroom_kostikshit_seen += 1
            "Это тумбочка с вещами твоего соседа."
            "Она как обычно заперта на замок."
            show me at left with dissolve
            me.c "Вероятно, он откроет её, когда выйдет из душа."
            jump start
        else:
            "Тумбочка заперта."
            jump start
        menu:
            "Подобрать":
                if not dormroom_bag:
                    me.c "И куда я это положу? Нужна сумка."
                    jump start
                else:
                    $ dormroom_kostikshit = True
                    $ dormroom_skillet = True
                    $ inventory.add_item("Сковородка", quantity=1)
                    "Ты подобрал сковородку."
                    jump start
            "Не подбирать":
                $ dormroom_kostikshit = True
                me.c "Ну на фиг."
                jump start

    if result == "dormroom_shower":
        if not dormroom_mystuff:
            if dormroom_shower_seen == 0:
                $ dormroom_shower_seen += 1
                "Ты заглядываешь в душ и видишь, как там полощется твой сосед."
                show me at left with dissolve
                me.c "Ладно."
                me.c "Пока что можно собрать вещи."
                jump start
            else:
                "Душ всё ещё занят."
                jump start
        else:
            $ dormroom_shower = True
            "Твой сосед как раз закончил умываться и впустил тебя внутрь."
            show me at left with dissolve
            me.c "Теперь надо как следует отдраиться!"
            "После пяти минут жесткой помывки ты чувствуешь себя посвежевшим и готовым к новым свершениям!"
            $ dormroom_kostik = False
            jump start

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
                jump start
            "Зачем ты украл сковородку?" if dormroom_skillet and not ask_1:
                $ ask_1 = True
                ko.c "Я просто забыл положить её обратно."
                with hpunch
                ko.c "Ты рылся в моих вещах!?"
                me.c "Я взял только сковородку!"
                jump start
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
                jump start

    if result == "dormroom_food":
        if not dormroom_shower:
            show me at left with dissolve
            me.c "Кушать, конечно, хочется, но сначала лучше принять душ."
            jump start
        if not dormroom_skillet:
            $ dormroom_food_seen += 1
            "Ты подходишь к вашей микрокухне с намерением приготовить яичницу."
            show me at left with dissolve
            me.c "А где сковородка?{w=0.5} Чёрт…"
            me.c "Я же только-только новую купил!"
            "Кажется, тебе придется довольствоваться чем-то другим."
            jump start
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
                jump start
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
                jump start

    if result == "dormroom_dressup":
        if dormroom_dressup_seen == 0:
            $ dormroom_dressup_seen += 1
            "Шкаф с твоими модными нарядами."
            "Сейчас твой гардероб сравнительно небольшой, но со временем ты сможешь его расширить!"
        if dormroom_shower == 0:
            me.c "Сначала, наверное, стоит принять душ, чтобы два раза не переодеваться."
            jump start
        else:
            $ dormroom_dressup = True
            me.c "Самое время выбрать себе наряд получше!"
            "Закончив с переодеванием, ты ещё раз осмотрел свою комнату."
            jump start

    if result == "dormroom_exit":
        show me at left with dissolve
        if not dormroom_shower:
            me.c "Преподы учуют запах раздолбая за километр."
            me.c "Пожалуй, перед выходом мне стоит принять душ."
            jump start
        elif not dormroom_mystuff:
            me.c "А как же мои вещи? Надо собраться!"
            jump start
        elif not dormroom_dressup:
            me.c "В таком виде я никуда не пойду."
            me.c "Для начала нужно одеться."
            jump start
        else:
            if not dormroom_food:
                "Твой живот урчит, требуя подзарядки."
            "После непродолжительных сборов ты толкаешь дверь и выходишь на улицу."
            jump start
