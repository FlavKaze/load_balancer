from unittest import TestCase
from load_balancer import  Machine, LoadBalancer
import os

class TestLoad(TestCase):
    def setUp(self):
        self.machine = Machine(2)
        self.load_balancer = LoadBalancer()

    def test_up_tasks(self):
        machine = Machine(2)
        self.assertEqual(self.machine.up_tasks(4, 1, 2), 0)

    def testando_a_maquina_executa_as_tasks_e_retorna_o_valor_das_que_n_conseguiu_executar(self):
        self.assertEqual(self.machine.up_tasks(4, 6, 2), 4)
        

    def testando_a_maquina_fecha_as_tasks_e_retorna_none(self):
        self.assertEqual(self.machine.close_processed_task(6), None)
        self.assertEqual(len(self.machine.tasks_death_tick), 0)

    def testando_a_maquina_o_valor_que_a_maquina_criou_na_lista(self):
        self.assertEqual(self.machine.up_tasks(4, 6, 2), 4)
        self.assertEqual(self.machine.tasks_death_tick[0], 6)

    def testando_se_adjust_list_retorna_a_lista_ajustada_coretamente(self):
        lista = [1,2,3,4]
        self.assertEqual(len(self.load_balancer.adjust_list(lista, 4)), 7)

    def testando_se_o_begin_process_adequa_as_variaveis_corretamente(self):
        self.load_balancer.begin_process()
        self.assertIsInstance(self.load_balancer.ticks, list)

    def testando_se_o_ttask_esta_maior_que_0_menor_que_11(self):
        self.load_balancer.begin_process()
        self.assertGreaterEqual(self.load_balancer.ttask, 1)
        self.assertLessEqual(self.load_balancer.ttask, 10)

    def testando_se_o_umax_esta_maior_que_0_menor_que_11(self):
        self.load_balancer.begin_process()
        self.assertGreaterEqual(self.load_balancer.umax, 1)
        self.assertLessEqual(self.load_balancer.umax, 10)

    def testando_se_input_existe(self):
        self.assertTrue(os.path.exists(self.load_balancer.input_file_name))
    
    def testando_se_output_e_criado(self):
        self.load_balancer.run()
        self.assertTrue(os.path.exists(self.load_balancer.output_file_name))