import urwid

class ButtonText(urwid.Text):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        urwid.Text.__init__(self, *args, **kwargs)
    def selectable(self):
        return True
    def keypress(self, size, key):
        if key == 'enter':
            self.callback(self.get_text())
        else:
            return key

class SingleEdit(urwid.Edit):
    def keypress(self, size, key):
        if key == 'enter':
            return urwid.Edit.keypress(self, size, 'down')
        else:
            return urwid.Edit.keypress(self, size, key)

class SingleIntEdit(urwid.IntEdit):
    def keypress(self, size, key):
        if key == 'enter':
            return urwid.Edit.keypress(self, size, 'down')
        else:
            return urwid.Edit.keypress(self, size, key)

class WordEdit(SingleEdit):
    def valid_char(self, ch):
        return urwid.Edit.valid_char(self, ch) and ch != ' '

class PassEdit(SingleEdit):
    def get_text(self):
        text = urwid.Edit.get_text(self)
        return (self.caption + " " * len(self.get_edit_text()), text[1])

class Wizard(urwid.WidgetWrap):
    def __init__(self):
        self.selected = None
        self.panels = []

        self.panelwrap = urwid.WidgetWrap( urwid.SolidFill() )
        self.back = urwid.Button("Back", self.back)
        self.next = urwid.Button("Next", self.next)
        self.buttons = urwid.Columns( [ self.back, self.next ], dividechars=3, focus_column=1 )
        pad = urwid.Padding( self.buttons, ('fixed right', 2), 19 )
        self.pile = urwid.Pile( [self.panelwrap, ('flow', pad)], 0 )
        urwid.WidgetWrap.__init__(self, self.pile)

    def add_panel(self, panel):
        self.panels.append( panel )
        if len(self.panels) == 1:
            self.select(0)
    
    def select(self, panelno, set_focus=True):
        if 0 <= panelno < len(self.panels):
            self.selected = panelno
            self.panelwrap.set_w( self.panels[panelno] )
            self.panels[panelno].activate()

            if set_focus:
                if self.panels[panelno].focusable():
                    self.pile.set_focus( 0 )
                else:
                    self.pile.set_focus( 1 )
    
    def next(self, *args, **kwargs):
        if self.panels[self.selected].check():
            self.select( self.selected )
            return
        self.select(self.selected + 1)
    
    def back(self, *args, **kwargs):
        self.select(self.selected - 1, False)

class WizardPanel(urwid.WidgetWrap):
    def __init__(self, state):
        self.state = state
        self.init_widgets()
        self.box = urwid.ListBox( urwid.SimpleListWalker( self.widgets ) )
        urwid.WidgetWrap.__init__( self, self.box )
    def init_widgets(self):
        self.widgets = []
    def focus_widget(self, widget):
        self.box.set_focus( self.widgets.index( widget ) )
    def focusable(self):
        return True
    def check(self):
        return
    def activate(self):
        return