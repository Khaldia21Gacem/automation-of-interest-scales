from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox, QTextEdit, QCheckBox
)
from PyQt5.QtGui import QDoubleValidator, QIcon
from PyQt5.QtCore import Qt
import sys
import locale

locale.setlocale(locale.LC_NUMERIC, '')


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oussama's Arithmétique calculator v2.0") 
        self.setGeometry(200, 200, 420, 400)
        self.light_mode = True
        self.set_dark_mode(False)
        self.setStyleSheet("font-family: Arial, sans-serif; font-size: 14px;")
        self.setWindowIcon(QIcon.fromTheme("calculator"))

        # Champs de saisie
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)
        self.input1.setFixedWidth(200)
        self.input2.setFixedWidth(200)
        validator = QDoubleValidator()
        self.input1.setValidator(validator)
        self.input2.setValidator(validator)
        self.input1.setPlaceholderText("Entrez le premier nombre")
        self.input2.setPlaceholderText("Entrez le deuxième nombre")
        self.input1.setToolTip("Saisissez un nombre décimal ou entier")
        self.input2.setToolTip("Saisissez un nombre décimal ou entier")

        # Résultat
        self.result_label = QLabel("Résultat : ", self)
        self.result_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        # Historique
        self.history_box = QTextEdit()
        self.history_box.setReadOnly(True)
        self.history_box.setPlaceholderText("Historique des opérations...")

        # Boutons opération
        self.add_btn = QPushButton(QIcon.fromTheme("list-add"), "+")
        self.sub_btn = QPushButton(QIcon.fromTheme("list-remove"), "-")
        self.mul_btn = QPushButton(QIcon.fromTheme("edit-copy"), "×")
        self.div_btn = QPushButton(QIcon.fromTheme("edit-cut"), "÷")
        self.equal_btn = QPushButton(QIcon.fromTheme("dialog-ok"), "=")
        self.equal_btn.setToolTip("Exécuter la dernière opération")


        # Boutons effacement
        self.clear_inputs_btn = QPushButton("C")
        self.clear_all_btn = QPushButton("Vider")

        for btn in [self.add_btn, self.sub_btn, self.mul_btn, self.div_btn, self.equal_btn,
                    self.clear_inputs_btn, self.clear_all_btn]:
            btn.setFixedSize(50, 50)

        self.add_btn.setToolTip("Additionner les deux nombres")
        self.sub_btn.setToolTip("Soustraire le deuxième nombre du premier")
        self.mul_btn.setToolTip("Multiplier les deux nombres")
        self.div_btn.setToolTip("Diviser le premier nombre par le deuxième")
        self.clear_inputs_btn.setToolTip("Effacer les champs de saisie")
        self.clear_all_btn.setToolTip("Réinitialiser tout")

        # Connexions
        self.last_operation = self.add
        self.add_btn.clicked.connect(lambda: self.set_operation(self.add))
        self.sub_btn.clicked.connect(lambda: self.set_operation(self.subtract))
        self.mul_btn.clicked.connect(lambda: self.set_operation(self.multiply))
        self.div_btn.clicked.connect(lambda: self.set_operation(self.divide))
        self.equal_btn.clicked.connect(self.execute_last_operation)
        self.clear_inputs_btn.clicked.connect(self.clear_inputs)
        self.clear_all_btn.clicked.connect(self.clear_all)
        self.input2.returnPressed.connect(self.execute_last_operation)


        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nombre 1 :"))
        layout.addWidget(self.input1)
        layout.addWidget(QLabel("Nombre 2 :"))
        layout.addWidget(self.input2)
        layout.setAlignment(Qt.AlignTop)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.sub_btn)
        btn_layout.addWidget(self.mul_btn)
        btn_layout.addWidget(self.div_btn)
        btn_layout.addWidget(self.equal_btn)

        clear_layout = QHBoxLayout()
        clear_layout.addWidget(self.clear_inputs_btn)
        clear_layout.addWidget(self.clear_all_btn)

        # 
        # Thème sombre
        self.theme_toggle = QCheckBox("Mode sombre")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        clear_layout.addWidget(self.theme_toggle)
        #
        # 
        layout.addLayout(btn_layout)
        layout.addWidget(self.result_label)
        layout.addLayout(clear_layout)
        layout.addWidget(QLabel("Historique :"))
        layout.addWidget(self.history_box)

        self.setLayout(layout)
    # 
    # Méthodes pour le thème sombre et clair
    def set_dark_mode(self, enabled):
        if enabled:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2e2e2e;
                    color: white;
                }
                QLineEdit, QTextEdit {
                    background-color: #444;
                    color: white;
                }
                QPushButton {
                    background-color: #555;
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: black;
                }
                QLineEdit, QTextEdit {
                    background-color: white;
                    color: black;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: black;
                }
            """)
    # 
    # Méthodes pour les opérations
    def toggle_theme(self, state):
        self.set_dark_mode(state == Qt.Checked)
    #
    # Méthodes pour la gestion des entrées et des résultats
    def get_inputs(self):
        text1 = self.input1.text().replace(",", ".").strip()
        text2 = self.input2.text().replace(",", ".").strip()
        if text1 == "" or text2 == "":
            QMessageBox.warning(self, "Erreur", "Veuillez remplir les deux champs.")
            return None, None
        return float(text1), float(text2)

    #
    # Méthodes pour afficher les résultats et l'historique
    def show_result(self, n1, n2, op, result):
        formatted_result = locale.format_string("%.2f", result, grouping=True)
        self.result_label.setText(f"Résultat : {formatted_result}")
        self.history_box.append(f"{n1} {op} {n2} = {formatted_result}")

    #
    # Méthodes pour la gestion des opérations
    def set_operation(self, operation):
        self.last_operation = operation
        operation()
    #
    # Méthode pour exécuter la dernière opération
    def execute_last_operation(self):
        if self.last_operation:
            self.last_operation()
    #
    # Méthodes pour les opérations arithmétiques
    # sum
    def add(self):
        n1, n2 = self.get_inputs()
        if n1 is not None:
            result = n1 + n2
            self.show_result(n1, n2, '+', result)
    #
    # Soustraction
    def subtract(self):
        n1, n2 = self.get_inputs()
        if n1 is not None:
            result = n1 - n2
            if n2 > n1:
                QMessageBox.warning(self, "Attention", "Le résultat sera négatif.")
            self.show_result(n1, n2, '-', result)
    #
    # Multiplication
    def multiply(self):
        n1, n2 = self.get_inputs()
        if n1 is not None:
            if n1 == 0 or n2 == 0:
                QMessageBox.warning(self, "Attention", "La multiplication par zéro donne toujours zéro.")
            result = n1 * n2
            self.show_result(n1, n2, '×', result)
    #
    # Division
    def divide(self):
        n1, n2 = self.get_inputs()
        if n1 is not None:
            if n2 == 0:
                QMessageBox.warning(self, "Erreur", "Division par zéro impossible.")
            else:
                result = n1 / n2
                self.show_result(n1, n2, '÷', result)
    #
    # Méthodes pour effacer les entrées et l'historique
    def clear_inputs(self):
        self.input1.clear()
        self.input2.clear()
    #
    # Méthode pour effacer tous les champs et l'historique
    def clear_all(self):
        self.input1.clear()
        self.input2.clear()
        self.result_label.setText("Résultat : ")
        self.history_box.clear()

# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())

