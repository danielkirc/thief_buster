#!/usr/bin/env python3
import wx

class PreviewPanel(wx.Panel):
    def __init__(self, parent, source):
        wx.Panel.__init__(self, parent)
        self.source = source

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        # Buffer
        sample_img = source.read()
        height, width = sample_img.shape[:2]
        self.bmp = wx.Bitmap.FromBuffer(width, height, sample_img)

        # Bind OnKey event
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)

        # Update on paint
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        # Timer
        self.timer = wx.Timer(self)
        self.timer.Start(1000./30)
        self.Bind(wx.EVT_TIMER, self.UpdateImage)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def UpdateImage(self, evt):
        self.bmp.CopyFromBuffer(self.source.read())
        self.Refresh()

    def OnKey(self, event):
        key_code = event.GetKeyCode()
        # Run once to detect code
        #print(key_code)

        # Exit on escape
        if key_code == wx.WXK_ESCAPE or key_code == 81:
            self.source.stop()
            self.Close(True)
        
        event.Skip()

    # Called on GUI exit (X btn)
    def OnExit(self):
        self.Close(True)

