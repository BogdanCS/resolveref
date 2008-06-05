#!/usr/bin/env python

# This file generated by a program. do not edit.
import Bio.EUtils.POM

#     
#                 This is the Current DTD for Entrez eLink
# $Id: eLink_020511.py,v 1.3 2007/07/21 14:55:33 mdehoon Exp $
# 
#  ================================================================= 
class ERROR(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  .+ 
class Info(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  .+ 
class Id(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))
	ATTLIST = Bio.EUtils.POM.AttributeList([Bio.EUtils.POM.XMLAttribute('HasLinkOut', ['Y', 'N'], 12, None), Bio.EUtils.POM.XMLAttribute('HasNeighbor', ['Y', 'N'], 12, None)])


#  \d+ 
class Score(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  \d+ 
class DbFrom(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  \S+ 
class DbTo(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  \S+ 
class LinkName(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  \S+ 
class IdList(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [(u'Id', u'*')], ''))


#  cmd=neighbor 
class Link(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'Id', ''), (u'Score', u'?')], ''))


class LinkSetDb(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'DbTo', ''), (u'LinkName', ''), (u'|', [(u'Link', u'*'), (u'Info', '')], ''), (u'ERROR', u'?')], ''))


#  cmd=links 
class Url(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  \S+ 
class IconUrl(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  \S+ 
class SubjectType(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  .+ 
class Attribute(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  .+ 
class Name(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  .+ 
class NameAbbr(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel(('', [('#PCDATA', '')], ''))


#  \S+ 
class Provider(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'Name', ''), (u'NameAbbr', ''), (u'Id', ''), (u'Url', ''), (u'IconUrl', u'?')], ''))


class ObjUrl(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'Url', ''), (u'LinkName', u'?'), (u'SubjectType', u'*'), (u'Attribute', u'*'), (u'Provider', '')], ''))


class IdUrlSet(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'Id', ''), (u'|', [(u'ObjUrl', u'+'), (u'Info', '')], '')], ''))


class IdUrlList(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'IdUrlSet', u'*'), (u'ERROR', u'?')], ''))


#  cmd=ncheck & lcheck 
class IdCheckList(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'Id', u'*'), (u'ERROR', u'?')], ''))


#  Common 
class LinkSet(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'DbFrom', ''), (u'|', [(u',', [(u'IdList', u'?'), (u'LinkSetDb', u'*')], ''), (u'IdUrlList', ''), (u'IdCheckList', ''), (u'ERROR', '')], '')], ''))


class eLinkResult(Bio.EUtils.POM.ElementNode):
	CONTENTMODEL = Bio.EUtils.POM.ContentModel((u',', [(u'LinkSet', u'+'), (u'ERROR', u'?')], ''))

