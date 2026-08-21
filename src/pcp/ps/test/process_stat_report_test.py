#!/usr/bin/env pmpython

import unittest
from unittest.mock import ANY, MagicMock, Mock, patch

from pcp_ps import PM_CONTEXT_ARCHIVE, ProcessStatReport, needs_previous_values


class TestProcessStatReport(unittest.TestCase):
    def _report(self, options, previous_values):
        group = MagicMock()
        group.__getitem__.return_value.netPrevValues = previous_values
        group.__getitem__.return_value.netValues = [object()]
        report = ProcessStatReport(group, options)
        report.Machine_info_count = 1
        return report

    def test_default_report_does_not_wait_for_previous_values(self):
        options = Mock(context=None, debug_mode=False, print_count=1,
                       selective_colum_flag=False, universal_flag='all')
        report = self._report(options, None)

        with patch.object(report, '_ProcessStatReport__get_timestamp', return_value='00:00:00'), \
             patch.object(report, 'timeStampDelta', side_effect=AttributeError), \
             patch.object(report, '_ProcessStatReport__print_report') as print_report, \
             self.assertRaises(SystemExit):
            report.report(Mock())

        print_report.assert_called_once_with(ANY, '00:00:00', '        ', '         ', 0)

    def test_user_report_waits_for_previous_values(self):
        options = Mock(context=None, debug_mode=False, print_count=1,
                       selective_colum_flag=False, universal_flag='user')
        report = self._report(options, None)

        self.assertFalse(report.report(Mock()))

    def test_archive_report_does_not_decrement_print_count(self):
        options = Mock(context=PM_CONTEXT_ARCHIVE, debug_mode=False,
                       print_count=1, selective_colum_flag=False,
                       universal_flag='all')
        report = self._report(options, object())

        with patch.object(report, '_ProcessStatReport__get_timestamp', return_value='00:00:00'), \
             patch.object(report, 'timeStampDelta', return_value=1.0), \
             patch.object(report, '_ProcessStatReport__print_report') as print_report:
            self.assertTrue(report.report(Mock()))

        self.assertEqual(options.print_count, 1)
        print_report.assert_called_once()

    def test_previous_values_are_only_needed_for_cpu_reports(self):
        default = Mock(universal_flag='all', selective_colum_flag=False)
        user = Mock(universal_flag='user', selective_colum_flag=False)
        columns = Mock(universal_flag='all', selective_colum_flag=True,
                       column_list=['pid', '%cpu'])

        self.assertFalse(needs_previous_values(default))
        self.assertTrue(needs_previous_values(user))
        self.assertTrue(needs_previous_values(columns))


if __name__ == '__main__':
    unittest.main()
