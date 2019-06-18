# coding: utf-8
import ROOT
import numpy 

infile = ROOT.TFile("/afs/cern.ch/user/k/kelong/work/WZAnalysis/CMSSW_10_6_0_patch1/src/Analysis/VVAnalysis/Zstudy_withScaleFacs.root")
infile.ls()
outfile = ROOT.TFile("fitPtZlep1.root", "recreate")
dydir = outfile.mkdir("DY")
dydir.cd()
#var = "ptl1"
var = "ZPt_mm"
inhist = infile.Get("DYm50/%s" % var)
sumweights = infile.Get("DYm50/sumweights").Integral()
inhist.Scale(35.9*1000*5765.4/sumweights)
#hist = ROOT.TH1D("ptl1_mm", "ptl1_mm", 80, 25, 80)
#print inhist.FindBin(25)
#for i in range(26, hist.GetNbinsX()+26):
#    hist.SetBinContent(i-25, inhist.GetBinContent(i))
hist = inhist.Clone()

errhistUp = hist.Clone(hist.GetName()+"_dummyErrUp")
errhistDown = hist.Clone(hist.GetName()+"_dummyErrDown")
for i in range(1, hist.GetNbinsX()+1):
    errhistDown.SetBinContent(i, hist.GetBinContent(i)*.95)
    errhistUp.SetBinContent(i, hist.GetBinContent(i)*1.05)
dydir.Write()
    
bkdir = outfile.mkdir("bkgd")
bkdir.cd()
bkhist = hist.Clone()
for i in range(1, hist.GetNbinsX()+1):
    bkhist.SetBinContent(i, hist.GetBinContent(i)*(hist.GetNbinsX()+1-i)*0.0005)
bkdir.Write()

datadir = outfile.mkdir("data_obs")
datadir.cd()
datahist = hist.Clone()
for i in range(1, hist.GetNbinsX()+1):
    rate = hist.GetBinContent(i) + bkhist.GetBinContent(i)
    smeared_rate = numpy.random.normal(rate, rate*0.03)

    datahist.SetBinContent(i, numpy.random.poisson(smeared_rate, 1)[0])
datadir.Write()

print "DY", hist.Integral()
print "bkgd", bkhist.Integral()
print "data", datahist.Integral()
