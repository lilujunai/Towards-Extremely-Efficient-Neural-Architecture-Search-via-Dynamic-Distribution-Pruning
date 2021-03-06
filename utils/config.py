import argparse
import os
from functools import partial
import torch
import time


def get_parser(name):
    """ make default formatted parser """
    parser = argparse.ArgumentParser(name, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # print default value always
    parser.add_argument = partial(parser.add_argument, help=' ')
    return parser


def parse_gpus(gpus):
    if gpus == 'all':
        return list(range(torch.cuda.device_count()))
    else:
        return [int(s) for s in gpus.split(',')]


class BaseConfig(argparse.Namespace):
    def print_params(self, prtf=print):
        prtf("")
        prtf("Parameters:")
        for attr, value in sorted(vars(self).items()):
            prtf("{}={}".format(attr.upper(), value))
        prtf("")

    def as_markdown(self):
        """ Return configs as markdown format """
        text = "|name|value|  \n|-|-|  \n"
        for attr, value in sorted(vars(self).items()):
            text += "|{}|{}|  \n".format(attr, value)

        return text


class SearchConfig(BaseConfig):
    def build_parser(self):
        parser = get_parser("Search config")
        parser.add_argument('--name', default='DDPNAS', required=False,
                            help='MDENAS / DDPNAS / SNG/ ASNG/ others will be comming soon')
        parser.add_argument('--sub_name', default='', required=False)
        parser.add_argument('--dataset', required=False, default='CIFAR10', help='CIFAR10 / MNIST / FashionMNIST')
        parser.add_argument('--datset_split', type=int, default=2, help='dataset split')
        parser.add_argument('--batch_size', type=int, default=512, help='batch size')
        parser.add_argument('--w_lr', type=float, default=0.025, help='lr for weights')
        parser.add_argument('--w_lr_step', type=int, default=2, help='lr for weights')
        parser.add_argument('--w_lr_min', type=float, default=0.001, help='minimum lr for weights')
        parser.add_argument('--w_momentum', type=float, default=0.9, help='momentum for weights')
        parser.add_argument('--w_weight_decay', type=float, default=3e-4,
                            help='weight decay for weights')
        parser.add_argument('--w_grad_clip', type=float, default=5.,
                            help='gradient clipping for weights')
        parser.add_argument('--print_freq', type=int, default=50, help='print frequency')
        parser.add_argument('--gpus', default='0', help='gpu device ids separated by comma. '
                            '`all` indicates use all gpus.')
        parser.add_argument('--epochs', type=int, default=200, help='# of training epochs')
        parser.add_argument('--warm_up_epochs', type=int, default=0, help='# of training epochs')
        parser.add_argument('--init_channels', type=int, default=16)
        parser.add_argument('--layers', type=int, default=8, help='# of layers')
        parser.add_argument('--n_nodes', type=int, default=4, help='# nodes in each cell')
        parser.add_argument('--seed', type=int, default=2, help='random seed')
        parser.add_argument('--workers', type=int, default=4, help='# of workers')
        # MDENAS learning rate
        parser.add_argument('--theta_lr', type=float, default=0.01, help='lr for theta')
        # DDPNAS
        parser.add_argument('--step', type=float, default=3, help='lr for theta')

        return parser

    def __init__(self):
        parser = self.build_parser()
        args = parser.parse_args()
        super().__init__(**vars(args))
        self.data_path = '/userhome/data/cifar10'
        time_str = time.asctime(time.localtime()).replace(' ', '_')
        self.path = os.path.join('/userhome/project/DDPNAS_V2/experiment', self.name + '_' + self.sub_name + '_' + time_str)
        # self.plot_path = os.path.join(self.path, 'plots')
        self.gpus = parse_gpus(self.gpus)
