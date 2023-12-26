from playwright.sync_api import Page

class TodoPage:
    """Page Object for the TodoMVC page."""
    
    def __init__(self, page: Page):
        """Constructor for the TodoPage class."""

        # The page object from Playwright.
        self.page = page

        # Input element to add todo items. This is a text box.
        self.entry = page.get_by_placeholder("What needs to be done?")

        # The list of todo items.
        self.todo_list = page.locator("ul.todo-list")

        # Checkbox to toggle all items betweeen completed and active. Disrespective of the view filter.
        self.toggle_all_checkbox = page.locator("css=section.main label").first

    def navigate(self):
        """Navigate to the TodoMVC page."""
        self.page.goto("http://todomvc.com/examples/react/")

    def add(self, *todos):
        """
        Add one or more todo items.

        Args:
            todos (str): The todo item(s) to be added. Multiple todo items can be passed.
        """
        for todo in todos:
            self.entry.fill(todo)
            self.entry.press("Enter")
            
    @property
    def entries(self):
        """Get all todo items."""
        return self.todo_list.get_by_role("listitem")
            
    def get_single_todo_item(self, todo):
        """
        Get a single todo item.

        Args:
            todo (str): The todo item to get.

        Returns:
            ElementHandle: The todo item.
        """
        return self.entries.filter(has_text=todo)
    
    def get_completed_todos(self):
        """
        Get all completed todo items.

        Returns:
            ElementHandle: The completed todo items.
        """
        return self.todo_list.locator("css=li.completed")
    
    def complete(self, todo):
        """
        Complete a todo item.

        Args:
            todo (str): The todo item to complete.
        """
        self.get_single_todo_item(todo).get_by_role('checkbox').check()

    def toggle_all(self):
        """Toggle all todo items."""
        self.toggle_all_checkbox.check()
