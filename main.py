#!/usr/bin/env python3
ProjectName = "Thief_buster"

# First found
v_source = 0
# External credentials file (v_source is string)
#from credentials import remote_server as v_source

# TODO: Save / restore faces
# TODO: Separate app to get all faces from a video
#from db_handler import DatabaseHandler

# Handle stream in another thread
from stream_handler import StreamHandler

import wx
from preview_panel import PreviewPanel

class MainApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, title=ProjectName)

        stream_handler = StreamHandler(v_source)
        stream_handler.start()

        prev_panel = PreviewPanel(frame, stream_handler)

        frame.Show()
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()

