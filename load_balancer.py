"""This script has to simulate a load-balancing task run on a cluster ."""

__author__ = ['Flavio Augusto Gaspareto']
__version__ = '1.0'
__maintainer__ = ['Flavio Augusto Gaspareto']
__email__ = ['flav.gaspareto@gmail.com']
__gitlab__ = ['https://gitlab.com/FlavKaze']

import os


class Machine:
    """Class that describes the attributes and methods of a machine / server.

    Attributes
    ----------
    tasks_death_tick : list
        List that keeps on which tick that process will end and will have to
        be removed from the machine.
    max_capacity : int
        Maximum limit of simultaneous tasks that the machine supports.
    open_tasks : int
        Number of open tasks.
    open_slots : int
        Number of slots for tesks available.
    """

    def __init__(self, umax: int):
        """Inicia a classe.

        :param umax:
        """
        self.tasks_death_tick = []
        self.max_capacity = umax
        self.open_tasks = 0
        self.open_slots = umax

    def close_processed_task(self, counter_tick: int) -> None:
        """Responsible for closing tasks marked to be killed on that tick.

        :param counter_tick: Counter of ticks from the beginning of
        the execution.
        """
        new_list = self.tasks_death_tick.copy()
        for each_task in self.tasks_death_tick:
            if each_task == counter_tick:
                new_list.remove(each_task)
                self.open_slots += 1
                self.open_tasks -= 1
        self.tasks_death_tick = new_list

    def up_tasks(self, counter_tick: int, number_tasks: int,
                 ttask: int) -> int:
        """Open the maximum number of processes called inside the machine.

        :param counter_tick: Counter of ticks from the beginning of
        the execution.
        :param number_tasks: Receive the number of tasks that you will try
        to open.
        :param ttask: Task size.
        :return: Returns the number of tasks not executed.
        """
        for each_task in range(number_tasks):
            if self.open_tasks < self.max_capacity:
                self.tasks_death_tick.append(counter_tick + ttask)
                self.open_tasks += 1
                self.open_slots -= 1
                number_tasks -= 1
            else:
                return number_tasks

        return 0


class LoadBalancer:
    """Class has the purpose of load balancing servers that run tasks.

    Attributes
    ----------
    open_machines : list
        List of machines that are open to perform tasks.
    ticks : list
        Receives the ticks to be processed in that execution.
    ttask : int
        Receives the size of the tasks for that execution.
    umax : int
        It receives the maximum value of tasks being executed simultaneously
        in that execution.
    input_file_name : str
        Name of the file that will be read to frame the entries.
    output_file_name : str
        Name of the file that will be written to the output.
    total_cost : int
        Variable that stores the cost spent on the machines being executed.
    last_machine_id : int
        Auxiliary variable to assist in the execution of the machines.
    """

    def __init__(self):
        """Inicia a classe."""
        self.open_machines = []
        self.ticks = None
        self.ttask = None
        self.umax = None
        self.input_file_name = "input.txt"
        self.output_file_name = "output.txt"
        self.total_cost = 0
        self.last_machine_id = 0

    def get_inputs(self) -> list:
        """Open the input file captures the lines and transforms in a list.

        :return: Returns a list of entries.
        """
        with open(self.input_file_name, "r")as file:
            lines = file.read()
            list_args = lines.split("\n")

        return list_args

    def set_output(self, current_costs: [list, str]) -> None:
        """Receives the cost on that tick and writes in file.

        :param current_costs: Parameter that waits the current cost to
        write to the file.
        """
        if isinstance(current_costs, list):
            str_costs = [str(x) for x in current_costs]
            line = ",".join(str_costs) + "\n"
        else:
            line = str(current_costs)
        with open(self.output_file_name, "a")as file:
            file.writelines(line)

    def begin_process(self) -> None:
        """Adjust the environment before starting the process."""
        list_args = self.get_inputs()

        self.ticks = [int(x) for x in list_args if x.isdigit()]

        if len(self.ticks) < 3:
            print("The input must have at least 3 lines with integers!")
            exit()

        self.ttask = self.ticks.pop(0)
        if self.ttask < 1 or self.ttask > 10:
            print("ttask must be greater than 0 and less than 11!")
            exit()

        self.umax = self.ticks.pop(0)
        if self.umax < 1 or self.umax > 10:
            print("umax must be greater than 0 and less than 11!")
            exit()

        self.ticks = self.adjust_list(self.ticks, self.ttask)

    @staticmethod
    def adjust_list(ticks: list, ttask: int) -> list:
        """Adjust the list that stores user tasks.

        :param ticks: Receive the list of ticks
        :param ttask: Receive the size of the default tasks.
        :return: Returns a list of tasks adjusted according to the input.
        """
        for _ in range(ttask - 1):
            ticks.append(0)
        return ticks

    def remove_machines(self, counter_tick: int) -> None:
        """Remove the tasks and removes machines no longer used.

        :param counter_tick: Counter of ticks from the beginning of
        the execution.
        """
        exclude_machine = []
        for each in self.open_machines:
            each.close_processed_task(counter_tick)
            if each.open_slots == self.umax:
                exclude_machine.append(each)

        for each in exclude_machine:
            self.open_machines.pop(self.open_machines.index(each))
            if self.last_machine_id > 0:
                self.last_machine_id -= 1

    def calculate_cost_and_call_output(self) -> None:
        """Calculate the cost of machines and calls to write to the output."""
        machines_open_tasks = []
        for each in self.open_machines:
            if each.open_tasks != 0:
                machines_open_tasks.append(
                    each.open_tasks)

        self.total_cost += len(machines_open_tasks)
        if not machines_open_tasks:
            machines_open_tasks.append(0)
        self.set_output(machines_open_tasks)

    def process(self) -> None:
        """Allocating the tacks on machines the smallest number possible."""
        for counter_tick, amount_task in enumerate(self.ticks, 1):

            self.remove_machines(counter_tick)

            if not self.open_machines and amount_task > 0:
                self.open_machines.append(Machine(self.umax))

            while amount_task:
                each_machine = self.open_machines[self.last_machine_id]

                amount_task = each_machine.up_tasks(
                    counter_tick,
                    amount_task,
                    self.ttask)
                if all([amount_task > 0,
                        each_machine.open_tasks == self.umax]):

                    self.open_machines.append(Machine(self.umax))
                    self.last_machine_id += 1

            self.calculate_cost_and_call_output()

        self.set_output(self.total_cost)

    def run(self) -> None:
        """Responsible for starting execution."""
        if os.path.exists(self.output_file_name):
            os.remove(self.output_file_name)
        self.begin_process()
        self.process()


if __name__ == "__main__":
    """
    Program start.
    """
    load_balancer = LoadBalancer()
    load_balancer.run()
