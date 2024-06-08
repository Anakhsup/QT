import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, \
    QMessageBox, QFileDialog, QDialog, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataInputDialog(QDialog):
    '''
    Создаем диалоговое окно для ввода данных (x и y) для построения графика
    QDialog создает диалоговое окно в PyQt5
    Светло-серый фон, отступом и шрифтом размера 14px, закругленные края, отступ
    QLabel Размер шрифта, внешний отступ внизу элемента
    border используется для задания стиля, толщины и цвета границы элемента
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-size: 14px;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 10px;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: black;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QVBoxLayout() # Создаем вертикальный макет (QVBoxLayout), который будет управлять расположением элементов в диалоговом окне

        self.x_label = QLabel("Enter the data for the X-axis (separated by commas):") # Создаем метки и поля ввода для данных оси X и Y
        layout.addWidget(self.x_label)

        self.x_edit = QLineEdit()
        layout.addWidget(self.x_edit)

        self.y_label = QLabel("Enter the data for the Y-axis (separated by commas):")
        layout.addWidget(self.y_label)

        self.y_edit = QLineEdit()
        layout.addWidget(self.y_edit)

        self.plot_button = QPushButton("Build a graph") # Создаем кнопку "Построить график" (QPushButton)
        self.plot_button.clicked.connect(self.accept)
        layout.addWidget(self.plot_button)

        self.setLayout(layout) # Устанавливает созданный макет (layout) как макет диалогового окна

    def get_data(self):
        return self.x_edit.text(), self.y_edit.text() # получаем данные, введенные пользователем, из диалогового окна

class MainWindow(QMainWindow):
    '''
    Главное окно приложения в PyQt5
    '''

    def __init__(self):
        '''
        QMainWindow Светло-желтый фон (#FFF8DC) и шрифт Arial без засечек
        QMenuBar Фиолетовый цвет с черным текстом
        '''
        super().__init__()
        self.setWindowTitle("Graphical application") # Устанавливаем заголовок окна на "Graphical application"
        self.setGeometry(100, 100, 800, 600) # Размер окна 100 на 100, 800 на 600 пикселей
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFF8DC;
                font-family: Arial, sans-serif;
            }
            QMenuBar {
                background-color: #8A2BE2;
                color: black;
                font-size: 16px;
            }
            QMenuBar::item {
                background-color: #8A2BE2;
                color: black;
            }
            QMenuBar::item::selected {
                background-color: #FFF5EE;
            }
            QMenu {
                background-color: #9932CC;
                color: black;
            }
            QMenu::item::selected {
                background-color: #FFF5EE;
            }
        """)

        self.create_menu() # Создаем меню приложения (файл, графики, дополнительные опции)
        self.show_message() # Отображает приветственное сообщение

    def set_view(self):
        self.scene = QGraphicsScene() # Сцена представляет собой контейнер для графических элементов, которые могут быть отображены
        self.view = QGraphicsView(self.scene) # Представляет собой виджет, который отображает содержимое графической сцены
        self.setCentralWidget(self.view) # self.view будет занимать основное пространство внутри главного окна и будет отображать содержимое, связанное с графической сценой self.scene

    def show_message(self):
        welcome_label = QLabel("You are welcome!")
        welcome_label.setAlignment(Qt.AlignCenter) # Устанавливаем выравнивание текста центру
        welcome_label.setStyleSheet("font-size: 18px; color: #333; padding: 20px;")
        self.setCentralWidget(welcome_label) # welcome_label займет центральное пространство главного окна

    def create_menu(self):
        main_menu = self.menuBar() # Создаем основное меню приложения

        file_menu = main_menu.addMenu("File")
        custom_graph_menu = main_menu.addMenu("Make your graph")

        # Добавляем пустое пространство, которое расширяется по мере необходимости, чтобы отодвинуть следующие элементы вправо
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_menu.setCornerWidget(spacer, Qt.TopRightCorner)

        additional_menu = main_menu.addMenu("More")
        graph_menu = main_menu.addMenu("Ready graphs")

        plot_linear_action = QAction("Linear graph", self)
        plot_linear_action.triggered.connect(self.plot_linear_graph)
        graph_menu.addAction(plot_linear_action)

        plot_sin_action = QAction("Sinus", self)
        plot_sin_action.triggered.connect(self.plot_sin_graph)
        graph_menu.addAction(plot_sin_action)

        plot_cos_action = QAction("Cosine", self)
        plot_cos_action.triggered.connect(self.plot_cos_graph)
        graph_menu.addAction(plot_cos_action)

        plot_quad_action = QAction("Square-law graph", self)
        plot_quad_action.triggered.connect(self.plot_quadratic_graph)
        graph_menu.addAction(plot_quad_action)

        plot_exp_action = QAction("Exponential graph", self)
        plot_exp_action.triggered.connect(self.plot_exponential_graph)
        graph_menu.addAction(plot_exp_action)

        plot_log_action = QAction("Logarithmic graph", self)
        plot_log_action.triggered.connect(self.plot_logarithmic_graph)
        graph_menu.addAction(plot_log_action)

        plot_scatter_action = QAction("Dot graph", self)
        plot_scatter_action.triggered.connect(self.plot_scatter_graph)
        graph_menu.addAction(plot_scatter_action)

        save_action = QAction(QIcon("save.png"), "Save graph", self)
        save_action.triggered.connect(self.save_graph)
        file_menu.addAction(save_action)

        export_data_action = QAction("Export data to CSV", self)
        export_data_action.triggered.connect(self.export_data_to_csv)
        file_menu.addAction(export_data_action)

        load_image_action = QAction("Upload graph", self)
        load_image_action.triggered.connect(self.load_image)
        file_menu.addAction(load_image_action)

        custom_plot_action = QAction("Using your data", self) # Создаем на основе введенных данных
        custom_plot_action.triggered.connect(self.show_custom_plot_dialog)
        custom_graph_menu.addAction(custom_plot_action)

        random_plot_action = QAction("Random graph", self)
        random_plot_action.triggered.connect(self.plot_random_graph)
        additional_menu.addAction(random_plot_action)

        reset_view_action = QAction("Reset the view", self)
        reset_view_action.triggered.connect(self.show_message)
        additional_menu.addAction(reset_view_action)

    def show_custom_plot_dialog(self):
        dialog = DataInputDialog(self) # Позволяем пользователю ввести данные для построения графика
        if dialog.exec_(): # Вызываем диалоговое окно и блокирует основное окно приложения до тех пор, пока пользователь не закроет диало
            x_data, y_data = dialog.get_data()
            self.plot_custom_graph(x_data, y_data) # Передаем полученные данные для построения пользовательского графика

    def plot_custom_graph(self, x_data, y_data):
        self.set_view()
        try:
            x_list = [float(x) for x in x_data.split(",")]
            y_list = [float(y) for y in y_data.split(",")]
            if len(x_list) != len(y_list):
                QMessageBox.warning(self, "Error", "The lengths of the data lists for X and Y must be the same.")
                return
            self.plot_graph(x_list, y_list, "Your graph", color='b')  # Синий цвет
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter the numeric data separated by commas.")

    def plot_linear_graph(self):
        self.set_view()
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        self.plot_graph(x, y, "Linear graph", color='r')  # Красный цвет

    def plot_sin_graph(self):
        self.set_view()
        x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        y = np.sin(x)
        self.plot_graph(x, y, "Sinus", color='g')  # Зеленый цвет

    def plot_cos_graph(self):
        self.set_view()
        x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        y = np.cos(x)
        self.plot_graph(x, y, "Cosine", color='b')  # Синий цвет

    def plot_quadratic_graph(self):
        self.set_view()
        x = np.linspace(-10, 10, 100)
        y = x ** 2
        self.plot_graph(x, y, "Square-law graph", color='m')  # Пурпурный цвет

    def plot_exponential_graph(self):
        self.set_view()
        x = np.linspace(0, 10, 100)
        y = np.exp(x)
        self.plot_graph(x, y, "Exponential graph", color='c')  # Голубой цвет

    def plot_logarithmic_graph(self):
        self.set_view()
        x = np.linspace(0.1, 10, 100)
        y = np.log(x)
        self.plot_graph(x, y, "Logarithmic graph", color='y')  # Желтый цвет

    def plot_scatter_graph(self):
        self.set_view()
        x = np.random.rand(100)
        y = np.random.rand(100)
        self.plot_scatter(x, y, "Dot graph", color='k')  # Черный цвет

    def plot_random_graph(self):
        self.set_view()
        x = np.linspace(0, 10, 100)
        y = np.random.rand(100)
        self.plot_graph(x, y, "Random graph", color='orange')  # Оранжевый цвет

    def plot_graph(self, x, y, title, color='b'):
        self.set_view()
        self.scene.clear()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, color=color)  # Изменение цвета графика
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)

        canvas = FigureCanvas(fig)
        canvas.draw()

        self.scene.addWidget(canvas)

    def plot_scatter(self, x, y, title, color='b'):
        self.set_view()
        self.scene.clear() # Очищаем текущую сцену, удаляя все ранее добавленные элементы

        fig = plt.figure()
        ax = fig.add_subplot(111) # 111 означает, что создается один подграфик, занимающий всю фигуру
        ax.scatter(x, y, color=color)  # Изменение цвета точек
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)

        canvas = FigureCanvas(fig) # Создаем холст для отображения графика
        canvas.draw()

        self.scene.addWidget(canvas) # Добавляем холст с графиком в сцену

    def save_graph(self):
        # Открываем диалоговое окно для сохранения файла
        file_name, _ = QFileDialog.getSaveFileName(self, "Save graph", "",
                                                   "PNG files (*.png);;JPEG files (*.jpg *.jpeg)")
        if file_name:
            plt.savefig(file_name)
            QMessageBox.information(self, "Success", "The schedule has been saved successfully!")

    def load_image(self):
        # Открываем диалоговое окно для выбора файла изображения, который нужно загрузить
        file_name, _ = QFileDialog.getOpenFileName(self, "Download graph", "", "Image files (*.png *.jpg *.jpeg)")
        if file_name:
            self.set_view()
            pixmap = QPixmap(file_name) # Загружаем изображение из указанного файла
            label = QLabel() # Создаем метки
            label.setPixmap(pixmap)
            self.scene.addWidget(label) # Добавляем метку с изображением в сцену
            QMessageBox.information(self, "Success", "The schedule has been saved successfully!")

    def export_data_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Export data", "",
                                                   "CSV files (*.csv)")
        if file_name:
            x = np.linspace(0, 10, 100)
            y = np.random.rand(100)
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["X", "Y"])
                writer.writerows(zip(x, y))
            QMessageBox.information(self, "Success", "The data has been successfully exported to CSV!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
