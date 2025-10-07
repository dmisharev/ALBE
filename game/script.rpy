define me = Character('Я', color="#c8ffc8")

init:
    define dormroom_dressup = 0
    define dormroom_exit = 0
    define dormroom_kostikshit = 0
    define dormroom_mystuff = 0
    define dormroom_shower = 0

    image dormroom = "dormroom.jpg"



# Интерактивный фон, состоящий из фона и интерактивных элементов (кнопок)
screen dormroom_screen:
    
    add "dormroom.jpg"

    if dormroom_bag == 0:
        imagebutton:
            auto "dormroom_bag_%s.png"
            focus_mask True
            xpos 948
            ypos 751
            action Return("dormroom_bag")

    if dormroom_dressup == 0:
        imagebutton:
            auto "dormroom_dressup_%s.png"
            focus_mask True
            xpos 1467
            ypos 479
            action Return("dormroom_dressup")

    if dormroom_exit == 0:
        imagebutton:
            auto "dormroom_exit_%s.png"
            focus_mask True
            xpos 0
            ypos 0
            action Return("dormroom_exit")

    if dormroom_kostikshit == 0:
        imagebutton:
            auto "dormroom_kostikshit_%s.png"
            focus_mask True
            xpos 482
            ypos 500
            action Return("dormroom_kostikshit")

    if dormroom_mystuff == 0:
        imagebutton:
            auto "dormroom_mystuff_%s.png"
            focus_mask True
            xpos 680
            ypos 305
            action Return("dormroom_mystuff")

    if dormroom_shower == 0:
        imagebutton:
            auto "dormroom_shower_%s.png"
            focus_mask True
            xpos 942
            ypos 191
            action Return("dormroom_shower")

label start:
    jump scene_1_0




label scene_1_0:
    $ save_name = ('Протокол отчисления. Сцена 1')
    $ renpy.block_rollback()
    $ renpy.pause(1, hard = True)

    scene dormroom
    call screen dormroom_screen
    $ result = _return

    if result == "dormroom_bag":

        "Ты поднимаешь с пола свою сумку."
        "Теперь у тебя появилась возможность носить с собой вещи!"
        me "Круто!"

        $ dormroom_bag = True

        jump scene_1_0

    if result == "dormroom_dressup":

        "Шкаф с твоими модными нарядами."
        "Сейчас твой гардероб сравнительно небольшой, но со временем ты сможешь его расширить!"

        if dormroom_shower == 0:
            me "Сначала, наверное, стоит принять душ, чтобы два раза не переодеваться."

            jump scene_1_0

        else:

            $ dormroom_dressup =+ 1

            me "Самое время выбрать себе наряд получше!"
            "Закончив с переодеванием, ты ещё раз осмотрел свою комнату."

            jump scene_1_0

    if result == "dormroom_exit":

        if dormroom_shower == 0:
            me "Преподы учуют запах раздолбая за километр."
            me "Пожалуй, перед выходом мне стоит принять душ."

            jump scene_1_0

        elif dormroom_mystuff == 0:
            me "А как же мои вещи? Надо собраться!"

            jump scene_1_0

        elif dormroom_dressup == 0:
            me "В таком виде я никуда не пойду."
            me "Для начала нужно одеться."

            jump scene_1_0

        else:
            "После непродолжительных сборов ты толкаешь дверь и выходишь на улицу."

    if result == "dormroom_kostikshit":
        "Это вещи твоего соседа. Их не стоит трогать."

        menu:

            "Подобрать":

                if not dormroom_bag:
                    me "И куда я это положу? Нужна сумка."

                else:

                    "Ты подобрал пистолет."

                    $ handgun = InventoryItem(
                        "Handgun", 
                        items_data["handgun"]["description"],
                        items_data["handgun"]["image"],
                        items_data["handgun"]["width"],
                        items_data["handgun"]["height"],
                        items_data["handgun"]["combinable"],
                        items_data["handgun"]["combine_with"],
                        items_data["handgun"]["result"]
                    )

                    $ re_inventory.add_item(handgun)

            "Не подбирать":
                me "Ну нафиг."

        jump scene_1_0

    if result == "dormroom_mystuff":
        "Ты подходишь к хаотично раскиданному хламу – твоим вещам."

        if not dormroom_bag:
            me "Так. Сначала надо найти, куда всё это сложить."

            jump scene_1_0

        else:

            $ dormroom_mystuff += 1

            "Ты складываешь всё необходимое в свою сумку."
            me "Так. А теперь что?"
            "Ты подобрал патроны."

            $ ammo = InventoryItem(
                "Handgun Ammo", 
                items_data["handgun_ammo"]["description"],
                items_data["handgun_ammo"]["image"],
                items_data["handgun_ammo"]["width"],
                items_data["handgun_ammo"]["height"],
                items_data["handgun_ammo"]["combinable"],
                items_data["handgun_ammo"]["combine_with"],
                items_data["handgun_ammo"]["result"]
            )

            $ re_inventory.add_item(ammo)

            jump scene_1_0

    if result == "dormroom_shower":

        if dormroom_mystuff == 0:

            "Ты заглядываешь в душ и видишь, как там полощется твой сосед."
            me "Ладно. Пока что соберу свои вещи."

            jump scene_1_0

        else:

            $ dormroom_shower += 1

            "Твой сосед как раз закончил умываться и впустил тебя внутрь."
            me "Чтож. Теперь надо как следует отдраиться!"
            "После пяти минут жесткой повывки ты чувствуешь себя посвежевшим и готовым к новым свершениям!"
            me "Надо поспешить, чтобы не опоздать в вуз!"

            jump scene_1_0