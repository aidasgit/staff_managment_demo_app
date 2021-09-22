class Employee:
    """Employee class"""

    def __init__(self, em_no, f_name, l_name, email="", salary=0, bonus=0):
        """employee class constructor if no email provided it generates unic email"""
        self.f_name = f_name
        self.l_name = l_name
        self.salary = salary
        self.em_no = em_no
        self.email = email
        self.bonus = bonus
        if not self.email:
            self.generate_unic_email()

    def __str__(self):
        """overrides default __str__ to be useful output function"""
        return "{}, {}, {}, {}, {:0.2f}".format(self.em_no, self.f_name, self.l_name, self.email, self.salary)

    def generate_unic_email(self):
        """Generates unic email"""
        self.email = self.f_name + "." + self.l_name + "." + self.em_no + "@cit.ie"
