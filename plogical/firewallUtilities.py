import sys
import subprocess
import shutil
import CyberCPLogFileWriter as logging
import argparse
import os
import shlex
import socket



class FirewallUtilities:

    @staticmethod
    def doCommand(command):
        import install as inst
        try:
            cmd = shlex.split(command)
            res = subprocess.call(cmd)
            if inst.preFlightsChecks.resFailed(inst.get_distro(), res):
                inst.preFlightsChecks.stdOut("Failed to apply rule: " + command + " Error #" + str(res), 1)
                return 0

        except OSError, msg:
            inst.preFlightsChecks.stdOut("Failed to apply rule: " + command + " Error: " + str(msg), 1)
            return 0
        except ValueError, msg:
            inst.preFlightsChecks.stdOut("Failed to apply rule: " + command + " Error: " + str(msg), 1)
            return 0

        return 1



    @staticmethod
    def addRule(proto,port,ipAddress):
        ruleFamily = 'rule family="ipv4"'
        sourceAddress = 'source address="' + ipAddress + '"'
        ruleProtocol = 'port protocol="' + proto + '"'
        rulePort = 'port="' + port + '"'

        command = "sudo firewall-cmd --permanent --zone=public --add-rich-rule='" + ruleFamily + " " + sourceAddress + " " + ruleProtocol + " " + rulePort + " " + "accept'"

        if not FirewallUtilities.doComamnd(command):
            return 0

        ruleFamily = 'rule family="ipv6"'
        sourceAddress = ''

        command = "sudo firewall-cmd --permanent --zone=public --add-rich-rule='" + ruleFamily + " " + sourceAddress + " " + ruleProtocol + " " + rulePort + " " + "accept'"

        if not FirewallUtilities.doComamnd(command):
            return 0

        command = 'sudo firewall-cmd --reload'

        if not FirewallUtilities.doComamnd(command):
            return 0

        return 1

    @staticmethod
    def deleteRule(proto, port, ipAddress):
        ruleFamily = 'rule family="ipv4"'
        sourceAddress = 'source address="' + ipAddress + '"'
        ruleProtocol = 'port protocol="' + proto + '"'
        rulePort = 'port="' + port + '"'

        command = "sudo firewall-cmd --permanent --zone=public --remove-rich-rule='" + ruleFamily + " " + sourceAddress + " " + ruleProtocol + " " + rulePort + " " + "accept'"

        if not FirewallUtilities.doComamnd(command):
            return 0

        ruleFamily = 'rule family="ipv6"'
        sourceAddress = ''

        command = "sudo firewall-cmd --permanent --zone=public --remove-rich-rule='" + ruleFamily + " " + sourceAddress + " " + ruleProtocol + " " + rulePort + " " + "accept'"

        if not FirewallUtilities.doComamnd(command):
            return 0

        command = 'sudo firewall-cmd --reload'

        ruleFamily = 'rule family="ipv6"'
        sourceAddress = ''

        command = "sudo firewall-cmd --permanent --zone=public --add-rich-rule='" + ruleFamily + " " + sourceAddress + " " + ruleProtocol + " " + rulePort + " " + "accept'"

        if not FirewallUtilities.doComamnd(command):
            return 0

        return 1
