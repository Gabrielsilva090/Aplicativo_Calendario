from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from idiomas.en.strings import translations as en_translations
from idiomas.pt.strings import translations as pt_translations
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle 
from kivy.core.window import Window
from kivy.config import Config
from kivy.app import App
import locale 
locale.setlocale(locale.LC_ALL, '') #alterar a linguagem do aplicativo com a do usuário


class BackgroundColorApp(MDApp): #mudar o fundo do aplicativo
    def build(self):
        return Builder.load_file('background.kv')



from database import Database #salvar as informações e puxa-lás do database
db = Database()


class ListItemWithCheckbox(TwoLineAvatarIconListItem): #marcar os itens selecionados e retirar a seleção 

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, the_list_item):
        if check.active == True:
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))

    def delete_item(self, the_list_item): #deleta um item da lista 
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass

class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    def show_date_picker(self): #aparece o calendário 
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):

        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)


class MainApp(MDApp):

    task_list_dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Purple" #tema geral do aplicativo
        self.icon = "calendario_logo.png"
    def show_task_dialog(self): #mostra a tela de dialógo quando apertar o botão de +
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(title="Criar Tarefa", type="custom", content_cls=DialogContent())
        self.task_list_dialog.open()

    def on_start(self):
        try:
            completed_tasks, uncomplete_tasks = db.get_tasks()
            print("completed_tasks", completed_tasks)
            print("uncompleted_task", uncomplete_tasks)


            if uncomplete_tasks != []:
                for task in uncomplete_tasks:
                    print("task :", task)
                    add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text='[s]'+task[1]+'[/s]', secondary_text=task[2])
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        
        except Exception as e:
            print(e)
            pass


    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date): #função para adicionar tarefas
        created_task = db.create_task(task.text, task_date)
        print("created_task ", created_task)
        self.root.ids.container.add_widget(ListItemWithCheckbox(pk=created_task[0], text='[b]'+created_task[1]+'[/b]', secondary_text=created_task[2]))
        task.text = ''


if __name__ == "__main__":
    MainApp().run()
    BackgroundColorApp().run()
