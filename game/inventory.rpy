# Resident Evil Inventory System for Ren'Py
# Save this in a separate .rpy file in your game directory

init python:
    # Inventory item class
    class InventoryItem:
        def __init__(self, name, description, image, width=1, height=1, combinable=False, combine_with=None, result=None):
            self.name = name
            self.description = description
            self.image = image
            self.width = width
            self.height = height
            self.combinable = combinable
            self.combine_with = combine_with  # List of items this can combine with
            self.result = result  # Result item after combination
        
        # Check if this item can combine with another
        def can_combine_with(self, other_item):
            if not self.combinable or not other_item.combinable:
                return False
            if other_item.name in self.combine_with:
                return True
            if self.name in other_item.combine_with:
                return True
            return False
        
        # Combine this item with another
        def combine(self, other_item):
            if self.can_combine_with(other_item):
                if self.result:
                    return InventoryItem(
                        self.result, 
                        items_data[self.result]["description"],
                        items_data[self.result]["image"],
                        items_data[self.result]["width"],
                        items_data[self.result]["height"],
                        items_data[self.result].get("combinable", False),
                        items_data[self.result].get("combine_with", []),
                        items_data[self.result].get("result", None)
                    )
            return None

    # Inventory system
    class REInventory:
        def __init__(self, rows=6, cols=8):
            self.rows = rows
            self.cols = cols
            self.grid = [[None for _ in range(cols)] for _ in range(rows)]
            self.items = []
            self.selected_item = None
            self.combine_mode = False
        
        # Check if an item fits at a position
        def can_place(self, item, row, col):
            if row + item.height > self.rows or col + item.width > self.cols:
                return False
            
            for r in range(row, row + item.height):
                for c in range(col, col + item.width):
                    if self.grid[r][c] is not None:
                        return False
            return True
        
        # Add item to inventory at first available position
        def add_item(self, item):
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.can_place(item, row, col):
                        self.place_item(item, row, col)
                        self.items.append(item)
                        return True
            return False  # No space
        
        # Place item at specific position
        def place_item(self, item, row, col):
            for r in range(row, row + item.height):
                for c in range(col, col + item.width):
                    self.grid[r][c] = item
        
        # Remove item from inventory
        def remove_item(self, item):
            if item in self.items:
                self.items.remove(item)
                # Clear the grid positions occupied by this item
                for row in range(self.rows):
                    for col in range(self.cols):
                        if self.grid[row][col] == item:
                            self.grid[row][col] = None
                return True
            return False
        
        # Get item at specific grid position
        def get_item_at(self, row, col):
            if 0 <= row < self.rows and 0 <= col < self.cols:
                return self.grid[row][col]
            return None
        
        # Find position of an item in the grid
        def find_item_position(self, item):
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.grid[row][col] == item:
                        return (row, col)
            return None
        
        # Select an item for examination/combination
        def select_item(self, item):
            if self.combine_mode and self.selected_item:
                # Try to combine items
                if self.selected_item != item and self.selected_item.can_combine_with(item):
                    result = self.selected_item.combine(item)
                    if result:
                        # Remove the original items
                        self.remove_item(self.selected_item)
                        self.remove_item(item)
                        # Add the result
                        self.add_item(result)
                        self.selected_item = None
                        self.combine_mode = False
                        return "combined"
                self.combine_mode = False
                self.selected_item = None
                return "failed_combine"
            else:
                self.selected_item = item
                return "selected"
        
        # Toggle combine mode
        def toggle_combine_mode(self):
            if self.selected_item and self.selected_item.combinable:
                self.combine_mode = not self.combine_mode
                return True
            return False
        
        # Rotate an item (swap width and height)
        def rotate_item(self, item):
            if item in self.items:
                pos = self.find_item_position(item)
                if pos:
                    row, col = pos
                    # Remove from current position
                    self.remove_item(item)
                    # Swap dimensions
                    item.width, item.height = item.height, item.width
                    # Try to place again
                    if self.can_place(item, row, col):
                        self.place_item(item, row, col)
                    else:
                        # If doesn't fit, revert dimensions and find new position
                        item.width, item.height = item.height, item.width
                        self.add_item(item)
                    return True
            return False

# Define some items
default items_data = {
    "handgun": {
        "description": "A standard 9mm handgun. Reliable and easy to handle.",
        "image": "images/inv_handgun.png",
        "width": 2,
        "height": 1,
        "combinable": True,
        "combine_with": ["handgun_ammo"],
        "result": "handgun_loaded"
    },
    "handgun_ammo": {
        "description": "A box of 9mm ammunition. Contains 15 rounds.",
        "image": "images/inv_handgun_ammo.png",
        "width": 1,
        "height": 1,
        "combinable": True,
        "combine_with": ["handgun"],
        "result": "handgun_loaded"
    },
    "handgun_loaded": {
        "description": "A loaded 9mm handgun. Ready to fire.",
        "image": "images/inv_handgun_loaded.png",
        "width": 2,
        "height": 1,
        "combinable": False
    },
    "first_aid_spray": {
        "description": "A medical spray that completely restores health.",
        "image": "images/inv_first_aid.png",
        "width": 1,
        "height": 2,
        "combinable": False
    }
}

# Initialize the inventory
default re_inventory = REInventory()

# Screen for the Resident Evil style inventory
screen re_inventory():
    tag menu
    modal True
    
    # Background - classic attaché case
    add "images/inv_background.jpg"
    
    # Inventory grid
    frame:
        background None
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 450
        
        # Grid background
        add "#00000080"  # Semi-transparent black
        
        # Draw grid cells
        for row in range(re_inventory.rows):
            for col in range(re_inventory.cols):
                $ cell_item = re_inventory.get_item_at(row, col)
                
                # Only draw the item in its top-left cell
                if cell_item and re_inventory.find_item_position(cell_item) == (row, col):
                    $ item = cell_item
                    imagebutton:
                        idle item.image
                        hover im.MatrixColor(item.image, im.matrix.brightness(0.2))
                        xpos col * 75
                        ypos row * 75
                        xsize item.width * 75
                        ysize item.height * 75
                        action [SetVariable("selected_item", item), Function(re_inventory.select_item, item)]
                        hovered SetVariable("hovered_item", item)
                        unhovered SetVariable("hovered_item", None)
                else:
                    # Empty cell or part of a larger item
                    if not cell_item:
                        add "images/inv_cell.png":
                            xpos col * 75
                            ypos row * 75
    
    # Item description panel
    frame:
        background "#321414"  # Dark red-brown
        xalign 0.5
        yalign 0.9
        xsize 600
        ysize 100
        
        if hovered_item:
            vbox:
                text hovered_item.name:
                    size 24
                    color "#FFFFFF"
                text hovered_item.description:
                    size 18
                    color "#CCCCCC"
        elif re_inventory.selected_item:
            vbox:
                text re_inventory.selected_item.name:
                    size 24
                    color "#FFFFFF"
                text re_inventory.selected_item.description:
                    size 18
                    color "#CCCCCC"
                if re_inventory.combine_mode:
                    text "Select another item to combine":
                        size 18
                        color "#FF5555"
        else:
            text "Select an item to examine it":
                size 24
                color "#AAAAAA"
                xalign 0.5
                yalign 0.5
    
    # Combine mode indicator
    if re_inventory.combine_mode:
        add "images/combine_mode.png":
            xalign 0.98
            yalign 0.02
    
    # Close button
    imagebutton:
        idle "images/button_close.png"
        hover "images/button_close_hover.png"
        xalign 0.98
        yalign 0.98
        action [Hide("re_inventory")]

# Default variables
default hovered_item = None
default selected_item = None

