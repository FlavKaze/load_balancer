"""
para teste unitarios

ttask tem q ser entre 1 e 10
umax tem q ser entre 1 e 10

input > remove > conta o tick > output

fila de saida =  en qual loop aquela task vai sair (especificar em qual server eles estava)

lista de servers

"""

class Machine:
    
    def __init__(self, umax):
        self.tasks_death_tick = []
        self.max_capacity = umax
        self.open_tasks = 0
        self.open_slots = umax

    def close_processed_task(self, counter_tick):
        for position, each_task in enumerate(self.tasks_death_tick, 0):
            if each_task == counter_tick:
                self.tasks_death_tick.pop(position)
                self.open_slots += 1
    
    def up_tasks(self, amount_task, number_tasks, ttask):
        for each_task in range(number_tasks):
            if self.open_tasks < self.max_capacity:
                self.tasks_death_tick.append(amount_task + (ttask - 1))
                self.open_tasks += 1
                number_tasks -= 1
            else:
                return number_tasks

        return 0


# 
    
    
class LoadBalancer:

    def __init__(self):
        self.open_machenes = []
        self.ticks = None
        self.ttask = None
        self.umax = None
        self.input_file_name = "input.txt"
        self.output_file_name = "output.txt"
        self.total_cost = 0

    def get_inputs(self):
        with open(self.input_file_name, "r")as file:
            lines = file.read()
            list_args = lines.split("\n")

        return list_args

    def set_output(self, current_costs):
        str_costs = [str(x) for x in current_costs]
        line = ",".join(str_costs)
        with open(self.output_file_name, "w")as file:
            file.write(line)

    def begin_process(self):
        list_args = self.get_inputs()

        #todos os ticks que irao executar
        self.ticks = [int(x) for x in list_args]
        #tamanho em ticks de uma tarefa
        self.ttask = self.ticks.pop(0)
        #numero maximo de usuarios por servidores
        self.umax = self.ticks.pop(0)
    
    def process(self):
        for counter_tick, amount_task in enumerate(self.ticks, 1):
            machines_open_tasks = []
            if not self.open_machenes and amount_task > 0:
                self.open_machenes.append(Machine(self.umax))
            
            for each_machine in self.open_machenes:
                while amount_task:
                    amount_task = each_machine.up_tasks(
                        counter_tick, 
                        amount_task, 
                        self.ttask)
                    if amount_task > 0:
                        self.open_machenes.append(Machine(self.umax))
                    else:
                        break
                
                each_machine.close_processed_task(counter_tick)
                machines_open_tasks.append(
                    each_machine.open_tasks)

            self.total_cost += sum(machines_open_tasks)
            self.set_output(machines_open_tasks)

    def run(self):
        self.begin_process()
        self.process()

if __name__ == "__main__":
    load_balancer = LoadBalancer()
    load_balancer.run()